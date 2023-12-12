import asyncio
import platform
import re
import shutil
import subprocess
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from logging import getLogger
from pathlib import Path
from sys import executable
from tempfile import TemporaryDirectory
from threading import Lock
from typing import Dict, List, Optional, TextIO, Tuple, Union, cast

from dask import config
from filelock import BaseFileLock, FileLock
from packaging.utils import parse_wheel_filename
from rich.progress import Progress
from typing_extensions import Literal

from coiled.context import track_context
from coiled.types import PackageInfo, PackageLevelEnum, ResolvedPackageInfo
from coiled.utils import (
    get_encoding,
    partition,
    recurse_importable_python_files,
    validate_wheel,
)
from coiled.v2.widgets.util import simple_progress

logger = getLogger("coiled.software_utils")
subdir_datas = {}
PYTHON_VERSION = platform.python_version_tuple()
ANY_AVAILABLE = "ANY-AVAILABLE"
COILED_LOCAL_PACKAGE_PREFIX = "coiled_local_"


async def create_subprocess_exec(
    program: str,
    *args: str,
    stdout: Union[TextIO, int, None] = None,
    stderr: Union[TextIO, int, None] = None,
) -> subprocess.CompletedProcess:
    # create_subprocess_exec is broken with IPython on Windows,
    # because it uses the wrong event loop
    loop = asyncio.get_running_loop()
    result = loop.run_in_executor(
        None, lambda: subprocess.run([program, *args], stdout=stdout, stderr=stderr, close_fds=True)
    )
    return await result


def partition_ignored_packages(
    packages: List[PackageInfo], priorities: Dict[Tuple[str, Literal["conda", "pip"]], PackageLevelEnum]
) -> Tuple[List[PackageInfo], List[PackageInfo]]:
    return partition(
        packages,
        lambda pkg: priorities.get((pkg["name"], pkg["source"])) == PackageLevelEnum.IGNORE,
    )


def partition_local_python_code_packages(packages: List[PackageInfo]) -> Tuple[List[PackageInfo], List[PackageInfo]]:
    return partition(
        packages,
        lambda pkg: pkg["name"].startswith(COILED_LOCAL_PACKAGE_PREFIX)
        and not cast(str, pkg["wheel_target"]).endswith(".whl"),
    )


def partition_local_packages(packages: List[PackageInfo]) -> Tuple[List[PackageInfo], List[PackageInfo]]:
    return partition(
        packages,
        lambda pkg: bool(pkg["wheel_target"]),
    )


class PackageBuildError(Exception):
    pass


WHEEL_BUILD_LOCKS: Dict[str, Tuple[BaseFileLock, Lock, TemporaryDirectory]] = {}


# filelock is thread local
# so we have to ensure the lock is acquired/released
# on the same thread
FILE_LOCK_POOL = ThreadPoolExecutor(max_workers=1)
THREAD_LOCK_POOL = ThreadPoolExecutor(max_workers=1)


@asynccontextmanager
async def async_lock(file_lock: BaseFileLock, thread_lock: Lock):
    # Beware, there are some complicated details to this locking implementation!
    # We're trying to manage the weirdness of the file lock mostly.
    loop = asyncio.get_event_loop()
    # first acquire a thread lock
    await loop.run_in_executor(THREAD_LOCK_POOL, thread_lock.acquire)
    # acquire the file lock, we should be the only thread trying to get it
    # the threadpool is required to release it, so another thread
    # attempting to get the lock will deadlock things by preventing the
    # release!
    await loop.run_in_executor(FILE_LOCK_POOL, file_lock.acquire)
    yield
    # release the file lock first
    await loop.run_in_executor(FILE_LOCK_POOL, file_lock.release)
    # now release the thread lock, allowing another thread to proceed
    # and get the file lock
    thread_lock.release()


@track_context
async def create_wheel(pkg_name: str, version: str, src: str) -> ResolvedPackageInfo:
    # These locks are set up such that
    # Threads: Block on each other and check if another thread already built the wheel
    # Processes: Block on each other, but will not reuse a wheel created by another
    # `pip wheel` is never run on the same package at the same time
    lock_path = Path(config.PATH)
    lock_path.mkdir(parents=True, exist_ok=True)  # ensure lockfile directory exists
    package_lock, thread_lock, tmpdir = WHEEL_BUILD_LOCKS.setdefault(
        pkg_name,
        (FileLock(lock_path / ("." + pkg_name + version + ".build-lock")), Lock(), TemporaryDirectory()),
    )
    async with async_lock(package_lock, thread_lock):
        outdir = Path(tmpdir.name) / Path(pkg_name)
        if outdir.exists():
            logger.debug(f"Checking for existing wheel for {pkg_name} @ {outdir}")
            wheel_fn = next((file for file in outdir.iterdir() if file.suffix == ".whl"), None)
        else:
            wheel_fn = None
        if not wheel_fn:
            logger.debug(f"No existing wheel, creating a wheel for {pkg_name} @ {src}")
            # must use executable to avoid using some other random python
            proc = await create_subprocess_exec(
                executable,
                "-m",
                "pip",
                "wheel",
                "--wheel-dir",
                str(outdir),
                "--no-deps",
                "--use-pep517",
                "--no-cache-dir",
                src,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
            )
            if proc.returncode:
                print(f"---Wheel Build Log for {pkg_name}---\n" + proc.stdout.decode(encoding=get_encoding()))
                return {
                    "name": pkg_name,
                    "source": "pip",
                    "channel": None,
                    "conda_name": None,
                    "client_version": version,
                    "specifier": "",
                    "include": False,
                    "error": (
                        "Failed to build a wheel for the"
                        " package, will not be included in environment, check stdout for the build log"
                    ),
                    "note": None,
                    "sdist": None,
                    "md5": None,
                }
            wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
        logger.debug(f"Using wheel @ {wheel_fn}")
        _, build_version, _, _ = parse_wheel_filename(str(wheel_fn.name))
        has_python, md5, missing_py_files = await validate_wheel(wheel_fn, src)
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": str(build_version),
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel contains no python files!",
        "note": (
            f"Wheel built from {src}"
            + (f" is missing {', '.join(sorted(missing_py_files)[:10])}" if missing_py_files else "")
        ),
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


@track_context
async def create_wheel_from_egg(pkg_name: str, version: str, src: str) -> ResolvedPackageInfo:
    tmpdir = TemporaryDirectory()
    outdir = Path(tmpdir.name) / Path(pkg_name)
    outdir.mkdir(parents=True)
    logger.debug(f"Attempting to create a wheel for {pkg_name} in directory {src}")
    # must use executable to avoid using some other random python
    proc = await create_subprocess_exec(
        executable,
        "-m",
        "wheel",
        "convert",
        "--dest-dir",
        str(outdir),
        src,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    if proc.returncode:
        print(f"---Egg to wheel conversion Log for {pkg_name}---\n" + proc.stdout.decode(encoding=get_encoding()))
        return {
            "name": pkg_name,
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": version,
            "specifier": "",
            "include": False,
            "error": (
                "Failed to convert the package egg to a wheel"
                ", will not be included in environment, check stdout for egg conversion log"
            ),
            "note": None,
            "sdist": None,
            "md5": None,
        }
    wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
    has_python, md5, missing_py_files = await validate_wheel(Path(wheel_fn), tmpdir.name)
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": version,
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel has no python files!",
        "note": (
            "Wheel built from local egg"
            + (f" is missing {', '.join(sorted(missing_py_files)[:10])}" if missing_py_files else "")
        ),
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


@track_context
async def create_wheel_from_src_dir(pkg_name: str, version: str, src: str) -> ResolvedPackageInfo:
    # These locks are set up such that
    # Threads: Block on each other and check if another thread already built the tarball
    # Processes: Block on each other, but will not reuse a tarball created by another
    md5 = None
    lock_path = Path(config.PATH)
    lock_path.mkdir(parents=True, exist_ok=True)  # ensure lockfile directory exists
    package_lock, thread_lock, tmpdir = WHEEL_BUILD_LOCKS.setdefault(
        pkg_name,
        (FileLock(lock_path / (f".{pkg_name}{version}.build-lock")), Lock(), TemporaryDirectory()),
    )
    async with async_lock(package_lock, thread_lock):
        outdir = Path(tmpdir.name) / Path(pkg_name)
        if outdir.exists():
            logger.debug(f"Checking for existing source archive for {pkg_name} @ {outdir}")
            wheel_fn = next((file for file in outdir.iterdir() if file.suffix == ".whl"), None)
        else:
            wheel_fn = None
        if not wheel_fn:
            logger.debug(f"No existing source archive, creating an archive for {pkg_name} @ {src}")
            try:
                unpacked_dir = outdir / f"{pkg_name}-{version}"
                # Create fake metadata to make wheel work
                dist_info_dir = unpacked_dir / f"{unpacked_dir.name}.dist-info"
                dist_info_dir.mkdir(parents=True)
                with open(dist_info_dir / "METADATA", "w") as f:
                    f.write(f"Metadata-Version: 2.1\nName: {pkg_name}\nVersion: {version}\n")
                with open(dist_info_dir / "WHEEL", "w") as f:
                    f.write("Wheel-Version: 1.0\nGenerator: coiled\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
                src_path = Path(src)
                for file in recurse_importable_python_files(src_path):
                    if str(file) in ("__init__.py", "__main__.py"):
                        continue
                    dest = unpacked_dir / file
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(src_path / file, dest)
                proc = await create_subprocess_exec(
                    executable,
                    "-m",
                    "wheel",
                    "pack",
                    "--dest-dir",
                    str(outdir),
                    str(unpacked_dir),
                    stderr=subprocess.STDOUT,
                    stdout=subprocess.PIPE,
                )
                if proc.returncode:
                    print(f"---wheel packing log for {src}---\n" + proc.stdout.decode(encoding=get_encoding()))
                    return {
                        "name": pkg_name,
                        "source": "pip",
                        "channel": None,
                        "conda_name": None,
                        "client_version": version,
                        "specifier": "",
                        "include": False,
                        "error": (
                            "Failed to build a package of your local python files. Please check stdout for details"
                        ),
                        "note": None,
                        "sdist": None,
                        "md5": None,
                    }
            except IOError as e:
                return {
                    "name": pkg_name,
                    "source": "pip",
                    "channel": None,
                    "conda_name": None,
                    "client_version": version,
                    "specifier": "",
                    "include": False,
                    "error": f"Failed to build a package of your local python files. Exception: {e}",
                    "note": None,
                    "sdist": None,
                    "md5": None,
                }
            wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
        logger.debug(f"Using wheel @ {wheel_fn}")
        _, build_version, _, _ = parse_wheel_filename(str(wheel_fn.name))
        has_python, md5, missing_py_files = await validate_wheel(wheel_fn, src)
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": str(build_version),
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel does not contain all python files!",
        "note": (
            f"Source wheel built from {src}"
            + (f" is missing {', '.join(sorted(missing_py_files)[:10])}" if missing_py_files else "")
        ),
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


async def create_wheels_for_local_python(packages: List[PackageInfo], progress: Optional[Progress] = None):
    finalized_packages: list[ResolvedPackageInfo] = []
    for pkg in packages:
        if pkg["wheel_target"]:
            with simple_progress(f'Creating wheel for {pkg["wheel_target"]}', progress=progress):
                finalized_packages.append(
                    await create_wheel_from_src_dir(
                        pkg_name=pkg["name"],
                        version=pkg["version"],
                        src=pkg["wheel_target"],
                    )
                )
    return finalized_packages


async def create_wheels_for_packages(
    packages: List[PackageInfo],
    progress: Optional[Progress] = None,
):
    finalized_packages: list[ResolvedPackageInfo] = []
    for pkg in packages:
        if pkg["wheel_target"]:
            if pkg["wheel_target"].endswith(".egg"):
                with simple_progress(f'Creating wheel from egg for {pkg["name"]}', progress=progress):
                    finalized_packages.append(
                        await create_wheel_from_egg(
                            pkg_name=pkg["name"],
                            version=pkg["version"],
                            src=pkg["wheel_target"],
                        )
                    )
            else:
                with simple_progress(f'Creating wheel for {pkg["name"]}', progress=progress):
                    finalized_packages.append(
                        await create_wheel(
                            pkg_name=pkg["name"],
                            version=pkg["version"],
                            src=pkg["wheel_target"],
                        )
                    )
    return finalized_packages


pip_bad_req_regex = (
    r"(?P<package>.+) (?P<version>.+) has requirement "
    r"(?P<requirement>.+), but you have (?P<requirement2>.+) (?P<reqversion>.+)."
)


@track_context
async def check_pip_happy(progress: Optional[Progress] = None) -> Dict[str, List[str]]:
    with simple_progress("Running pip check", progress=progress):
        proc = await create_subprocess_exec(
            executable, "-m", "pip", "check", stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        faulty_packages = defaultdict(list)
        if proc.returncode:
            output = proc.stdout.decode(encoding=get_encoding())
            bad_reqs = re.finditer(pip_bad_req_regex, output)
            for bad_req in bad_reqs:
                groups = bad_req.groupdict()
                span = bad_req.span()
                warning = output[span[0] : span[1]]
                logger.warning(warning)
                faulty_packages[groups["package"]].append(warning)
        return faulty_packages

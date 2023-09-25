import hashlib
import os
import shutil
import subprocess
import typing

import fv3config
import pytest

from pathlib import Path


CONFIG_DIR = Path(__file__).parent
EXECUTABLE = Path("/SHiELD/SHiELD_build/Build/bin/SHiELD_nh.prod.64bit.gnu.x")


def get_config(filename):
    config_filename = CONFIG_DIR / filename
    with open(config_filename, "r") as f:
        return fv3config.load(f)
    

def checksum_file(path: Path) -> str:
    sum = hashlib.md5()
    BUFFER_SIZE = 1024 * 1024
    with open(path, "rb") as f:
        while True:
            buf = f.read(BUFFER_SIZE)
            if not buf:
                break
            sum.update(buf)
    return sum.hexdigest()


def get_rundir_netcdfs(rundir: Path) -> typing.List[Path]:
    restart_directory = rundir / "RESTART"
    diagnostics_files = sorted(rundir.glob("*.nc"))
    restart_files = sorted(restart_directory.glob("*.nc"))
    return diagnostics_files + restart_files    


def checksum_rundir_to_dict(rundir: Path) -> typing.Dict[str, str]:
    rundir_netcdfs = get_rundir_netcdfs(rundir)
    return {file.name: checksum_file(file) for file in rundir_netcdfs}


def checksum_rundir_to_file(rundir: Path, file: Path):
    """checksum rundir storing output in file"""
    rundir_netcdfs = get_rundir_netcdfs(rundir)
    for path in rundir_netcdfs:
        print(path, checksum_file(path), file=file)


def _run_simulation(config: dict, rundir: Path, command: typing.List[str]):
    fv3config.write_run_directory(config, rundir)
    n_processes = fv3config.config.get_n_processes(config)
    command = ["mpirun", "-n", str(n_processes)] + command
    completed_process = subprocess.run(command, cwd=rundir, capture_output=True)
    if completed_process.returncode != 0:
        print("Tail of Stderr:")
        print(completed_process.stderr[-2000:].decode())
        print("Tail of Stdout:")
        print(completed_process.stdout[-2000:].decode())
        pytest.fail()
    return completed_process
    
        
def run_fortran_executable(config: dict, rundir: Path):
    command = [EXECUTABLE.absolute().as_posix()]
    return _run_simulation(config, rundir, command)    


def test_regression_fortran(tmp_path: Path, regtest):
    """Quickly test that the executable produces an identical result
    with previous build.
    """
    config = get_config("default.yml")
    rundir = tmp_path / "rundir"

    run_fortran_executable(config, rundir)
    checksum_rundir_to_file(rundir, file=regtest)


# def test_reproducibility(tmp_path: Path, regtest):
#     """Test that the executable repeatedly produces the same result. This also
#     tests that results are reproducible across builds, but is slower."""
#     config = get_config("default.yml")
#     rundir = tmp_path / "rundir"

#     for i in range(5):
#         run_fortran_executable(config, rundir)
#         if i == 0:
#             expected = checksum_rundir_to_dict(rundir)
#         else:
#             result = checksum_rundir_to_dict(rundir)
#             assert result == expected
#         if i < 4:
#             # Preserve the run directory from the last iteration to log the
#             # checksums with regtest.
#             shutil.rmtree(rundir)

#     checksum_rundir_to_file(rundir, file=regtest)
        

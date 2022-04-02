from pathlib import Path
from tempfile import TemporaryDirectory

from ..report import check_VASP_job_status, check_FEFF_job_status


def test_check_VASP_job_status_success(dummyVASPOUTCARSuccess):
    with TemporaryDirectory() as tempdir:
        name = Path(tempdir) / Path("OUTCAR")
        with open(name, "w") as f:
            f.write(dummyVASPOUTCARSuccess)
        assert name.exists()
        assert check_VASP_job_status(tempdir)


def test_check_VASP_job_status_fail(dummyVASPOUTCARFailure):
    with TemporaryDirectory() as tempdir:
        name = Path(tempdir) / Path("OUTCAR")
        with open(name, "w") as f:
            f.write(dummyVASPOUTCARFailure)
        assert name.exists()
        assert not check_VASP_job_status(tempdir)


def test_check_FEFF_job_status_success(dummyFEFFSuccess):
    feff, xmu = dummyFEFFSuccess
    with TemporaryDirectory() as tempdir:
        name1 = Path(tempdir) / Path("feff.out")
        with open(name1, "w") as f:
            f.write(feff)
        name2 = Path(tempdir) / Path("xmu.dat")
        with open(name2, "w") as f:
            f.write(xmu)
        assert name1.exists()
        assert name2.exists()
        assert check_FEFF_job_status(tempdir)


def test_check_FEFF_job_status_failure_empty_xmu(dummyFEFFFailure):
    feff, xmu = dummyFEFFFailure
    with TemporaryDirectory() as tempdir:
        name = Path(tempdir) / Path("xmu.dat")
        with open(name, "w") as f:
            f.write(xmu)
        assert name.stat().st_size == 0
        assert name.exists()
        assert not check_FEFF_job_status(tempdir)


def test_check_FEFF_job_status_failure(dummyFEFFFailure, dummyFEFFSuccess):
    feff, _ = dummyFEFFFailure
    _, xmu = dummyFEFFSuccess
    with TemporaryDirectory() as tempdir:
        name1 = Path(tempdir) / Path("feff.out")
        with open(name1, "w") as f:
            f.write(feff)
        name2 = Path(tempdir) / Path("xmu.dat")
        with open(name2, "w") as f:
            f.write(xmu)
        assert name1.exists()
        assert name2.exists()
        assert not check_FEFF_job_status(tempdir)

from pathlib import Path


from ..file_utils import exhaustive_directory_search
from ..report import (
    generate_report,
    check_computation_type,
)


def test_generate_report(DummyDirectories):
    with DummyDirectories() as tmpdir:
        report = generate_report(tmpdir, "submit.sbatch")
        assert len(report["VASP"]["success"]) == 1
        assert len(report["VASP"]["fail"]) == 0
        assert len(report["FEFF"]["success"]) == 1
        assert len(report["FEFF"]["fail"]) == 0


def test_check_computation_type(DummyDirectories):
    with DummyDirectories() as tmpdir:
        directories = exhaustive_directory_search(tmpdir, "submit.sbatch")
        d = {Path(dd): check_computation_type(dd) for dd in directories}
        for key, value in d.items():
            if "vasp-like" in str(key):
                assert value == "VASP"
            elif "feff-like" in str(key):
                assert value == "FEFF"
            else:
                assert value is None

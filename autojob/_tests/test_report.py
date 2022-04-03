from pathlib import Path


from ..file_utils import exhaustive_directory_search
from ..report import (
    generate_report,
    check_computation_type,
)


def test_generate_report(DummyDirectories):
    with DummyDirectories() as tmpdir:
        report = generate_report(tmpdir, "submit.sbatch")
        for d, v in report.items():
            cond = "success" in d.parts[-2]
            assert cond == v


def test_check_computation_type(DummyDirectories):
    with DummyDirectories() as tmpdir:
        directories = exhaustive_directory_search(tmpdir, "submit.sbatch")
        d = {Path(dd): check_computation_type(dd) for dd in directories}
        assert all([value in key.parts[-2] for key, value in d.items()])

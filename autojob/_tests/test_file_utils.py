from pathlib import Path

from ..file_utils import exhaustive_directory_search


def test_exhaustive_directory_search(dummydirectories):
    with dummydirectories as tmpdir:
        d = exhaustive_directory_search(tmpdir, "submit.sbatch")
        for dd in d:
            assert "mp-390" not in Path(dd).parts[-2:]

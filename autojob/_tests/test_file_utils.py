from pathlib import Path
from tempfile import TemporaryDirectory

from ..file_utils import exhaustive_directory_search, run_command


def test_exhaustive_directory_search(dummydirectories):
    with dummydirectories as tmpdir:
        d = exhaustive_directory_search(tmpdir, "submit.sbatch")
        for dd in d:
            assert "mp-390" not in Path(dd).parts[-2:]


def test_run_command():
    with TemporaryDirectory() as tempdir:
        name = Path(tempdir) / Path("aintnothingbutaheartache.txt")
        ex = f"touch {str(name)}"
        run_command(ex)
        assert name.exists()

from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from ..file_utils import (
    exhaustive_directory_search,
    run_command,
    read_json,
    save_json,
)


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


def test_save_read_json():
    dummy_dictionary = {str(uuid4()): str(uuid4()) for _ in range(10)}
    with TemporaryDirectory() as tempdir:
        name1 = Path(tempdir) / Path("tmp1.json")
        save_json(dummy_dictionary, name1)
        name2 = Path(tempdir) / Path("tmp2.json")
        save_json(dummy_dictionary, name2, indent=2, sort_keys=True)
        dummy_dictionary1 = read_json(name1)
        dummy_dictionary2 = read_json(name2)
    assert dummy_dictionary == dummy_dictionary1
    assert dummy_dictionary == dummy_dictionary2

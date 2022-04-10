from pathlib import Path
import pytest
import random
import string
from tempfile import TemporaryDirectory
from uuid import uuid4

LETTERS = string.ascii_lowercase
OUTCAR_TEST_LINE = " General timing and accounting informations for this job:"
FEFFOUT_TEST_LINE = "feff ends at"


def write_random_lines(filename, n=40, inject=None):
    """Writes a bunch of random lines to the provided file buffer.

    Parameters
    ----------
    filename : os.PathLike
        Filename to save to.
    n : int, optional
        The number of random lines to write. Default is 40.
    inject : str, optional
        If not None, injects this string in a random place.
    """

    inject_location = None
    if inject is not None:
        inject_location = random.randint(0, n - 1)

    with open(filename, "w") as f:
        for ii in range(n):
            if inject_location is not None and ii == inject_location:
                f.write(f"{inject}\n")
                continue
            line = [random.choice(LETTERS) for _ in range(10)]
            line = line * random.randint(1, 4)
            f.write(f"{''.join(line)}\n")


class _DummyDirectories(TemporaryDirectory):
    """A helper utility class for temporarily creating a large directory
    structure for tests to be conducted in. Will cleanup when done."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculations = {
            "test1": ["test.txt", "input.txt", "LOG", "submit.sbatch"],
            "test2": ["INCAR", "POTCAR", "output.out", "submit.sbatch"],
            "test3_vasp-like": [
                "INCAR",
                "POSCAR",
                "KPOINTS",
                "POTCAR",
                "OUTCAR",
                "submit.sbatch",
            ],
            "test4_feff-like": [
                "feff.inp",
                "feff.out",
                "xmu.dat",
                "submit.sbatch",
            ],
            "test_no_submit": ["test_input.txt", "test_input2.txt"],
        }

    def __enter__(self):
        """Constructs a dummy directory structure for testing methods that act
        on various files. This also creates the dummy directory structures."""

        # The parent __enter__ method will actually create the dummy directory
        # and return the path to it
        name = super().__enter__()

        for key, value in self.calculations.items():
            path = Path(name) / Path(str(uuid4())) / Path(key)
            path.mkdir(exist_ok=False, parents=True)

            for filename in value:
                target = path / filename
                if filename == "OUTCAR":
                    write_random_lines(target, 40, OUTCAR_TEST_LINE)
                elif filename == "feff.out":
                    write_random_lines(target, 40, FEFFOUT_TEST_LINE)
                elif filename == "xmu.dat":
                    write_random_lines(target, 40)
                else:
                    (path / Path(target)).touch()

        return name


@pytest.fixture
def DummyDirectories():
    return _DummyDirectories

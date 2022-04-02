from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

ABS_PATH = Path(Path(__file__).resolve().parent)


class DummyDirectories(TemporaryDirectory):
    """A helper utility class for temporarily creating a large directory
    structure for tests to be conducted in. Will cleanup when done. The
    directories used are actually based on real input files using VASP, FEFF,
    etc."""

    def __enter__(self):
        """Constructs a dummy directory structure for testing methods that act
        on input files."""

        name = super().__enter__()

        d1 = [
            "mp-1179358",
            "mp-636827",
            "mvc-11423",
            "mp-25433",
            "mp-655656",
            "mvc-11600",
            "mp-390",
            "mp-685151",
        ]

        d2 = ["FEFF-XANES", "VASP"]

        input_files = {
            "FEFF-XANES": ["feff.inp"],
            "VASP": ["INCAR", "KPOINTS", "POSCAR", "POTCAR"],
        }

        for x1 in d1:
            for x2 in d2:
                path = Path(name) / Path(f"{x1}/{x2}")
                path.mkdir(parents=True, exist_ok=False)

                for inp in input_files[x2]:
                    (path / Path(inp)).touch()

                # Write the dummy submit scripts for everything except for
                # mp-390
                if x1 != "mp-390":
                    (path / Path("submit.sbatch")).touch()

        return name


@pytest.fixture
def dummyFullDirectoryStructure():
    return DummyDirectories()


@pytest.fixture
def dummyVASPOUTCARFailure():
    d = ABS_PATH / Path("dummy_files") / Path("failure")
    with open(d / Path("OUTCAR"), "r") as f:
        lines = f.readlines()
    return "".join(lines)


@pytest.fixture
def dummyVASPOUTCARSuccess():
    d = ABS_PATH / Path("dummy_files") / Path("success")
    with open(d / Path("OUTCAR"), "r") as f:
        lines = f.readlines()
    return "".join(lines)


@pytest.fixture
def dummyFEFFSuccess():
    d = ABS_PATH / Path("dummy_files") / Path("success")
    with open(d / Path("feff.out"), "r") as f:
        lines = f.readlines()
    with open(d / Path("xmu.dat"), "r") as f:
        lines_xmu = f.readlines()
    return "".join(lines), "".join(lines_xmu)


@pytest.fixture
def dummyFEFFFailure():
    d = ABS_PATH / Path("dummy_files") / Path("failure")
    with open(d / Path("feff.out"), "r") as f:
        lines = f.readlines()
    with open(d / Path("xmu.dat"), "r") as f:
        lines_xmu = f.readlines()
    return "".join(lines), "".join(lines_xmu)

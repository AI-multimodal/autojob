from pathlib import Path
import pytest
from tempfile import TemporaryDirectory
from uuid import uuid4

ABS_PATH = Path(Path(__file__).resolve().parent)


class _DummyDirectories(TemporaryDirectory):
    """A helper utility class for temporarily creating a large directory
    structure for tests to be conducted in. Will cleanup when done. The
    directories used are actually based on real input files using VASP, FEFF,
    etc."""

    @staticmethod
    def _get_dummy_file(success, filename):
        root = ABS_PATH / Path("dummy_files")
        d = root / Path("success" if success else "failure")
        with open(d / Path(filename), "r") as f:
            lines = f.readlines()
        return "".join(lines)

    @staticmethod
    def _write_dummy_file(path, success, filename):
        string = _DummyDirectories._get_dummy_file(success, filename)
        # print(path, success, filename, string.split("\n")[-10:])
        with open(path, "w") as f:
            f.write(string)

    @staticmethod
    def _write_VASP_inputs(root, success=True):
        """Helper method for "writing" the fake VASP input files.

        Parameters
        ----------
        root : os.PathLike
            Directory to save in.
        success : bool, optional
            If True, then writes the successful files.
        has_submit_script : bool, optional
            Description

        """

        for inp in ["INCAR", "KPOINTS", "POSCAR", "POTCAR"]:
            (Path(root) / Path(inp)).touch()

        _DummyDirectories._write_dummy_file(
            Path(root) / Path("OUTCAR"), success, "OUTCAR"
        )

    @staticmethod
    def _write_FEFF_inputs(root, success=True):
        """Helper method for "writing" the fake FEFF input files.

        Parameters
        ----------
        root : os.PathLike
        """

        for inp in ["feff.inp"]:
            (Path(root) / Path(inp)).touch()

        _DummyDirectories._write_dummy_file(
            Path(root) / Path("feff.out"), success, "feff.out"
        )
        _DummyDirectories._write_dummy_file(
            Path(root) / Path("xmu.dat"), success, "xmu.dat"
        )

    def __enter__(self):
        """Constructs a dummy directory structure for testing methods that act
        on input files."""

        name = super().__enter__()

        # Write a special directory for just checking that the exhaustive
        # search method doesn't check directories without submit.sbatch
        path = Path(name) / Path("no-submit-script") / Path(str(uuid4()))
        path.mkdir(parents=True, exist_ok=False)
        _DummyDirectories._write_VASP_inputs(path, success=True)

        for failstate in [True, False]:
            failstate_str = "success" if failstate else "failure"

            for calc in ["FEFF", "VASP"]:
                p1 = Path(name) / Path(f"{calc}-{failstate_str}")
                path = p1 / Path(str(uuid4()))
                path.mkdir(parents=True, exist_ok=False)

                if calc == "FEFF":
                    _DummyDirectories._write_FEFF_inputs(path, failstate)
                elif calc == "VASP":
                    _DummyDirectories._write_VASP_inputs(path, failstate)
                else:
                    raise RuntimeError

                (path / Path("submit.sbatch")).touch()

        return name


@pytest.fixture
def DummyDirectories():
    return _DummyDirectories

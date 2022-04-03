from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


CONFIG = {
    "report.in": {
        "FEFF": ["feff.inp"],
        "VASP": ["INCAR", "POSCAR", "KPOINTS", "POTCAR"],
    },
    "report.out": {
        "FEFF": [["xmu.dat", None], ["feff.out", "feff ends at"]],
        "VASP": [
            [
                "OUTCAR",
                " General timing and accounting informations for this job:",
            ]
        ],
    },
}

"""PPM 2 / immers Python wrapper.

Units
-----
This package does **not** inspect or convert coordinate units.

Input PDBs passed to immers (``run_and_clean``, ``run_wrapped_immers``,
the ``ppm2 run`` CLI) are assumed to be in **ångström**, the PDB
format default. immers reads the coordinate columns as Å and writes
placement lengths in Å. There is no check.

``PPMReport`` / ``PlacementData`` lengths are therefore always Å:

- ``hydrophobic_thickness``, ``hydrophobic_depth`` — Å
- ``membrane_z`` (midplane, lower, upper, half_thickness) — Å
- ``tilt_angle``, ``tilt_angle_err`` — degrees
- ``transfer_energy`` — kcal/mol

Cartesian orientation lives in the immers ``oriented.pdb``, not on this
report. ``mdtraj.load`` stores those coordinates in **nm**.
"""

from .wrapper import (
    run_wrapped_immers,
    run_wrapped_immers_plain,
    ImmersPlainOutput,
    PlacementData,
    MembraneZ,
    SubunitSegment,
    Subunit,
    TransmembraneRegions,
    ImmersOutput,
    Topology,
    PPMReport,
    run_and_clean,
)

__version__ = "0.0.0"


__all__ = [
    "run_wrapped_immers",
    "run_wrapped_immers_plain",
    "ImmersPlainOutput",
    "PlacementData",
    "MembraneZ",
    "SubunitSegment",
    "Subunit",
    "TransmembraneRegions",
    "ImmersOutput",
    "Topology",
    "PPMReport",
    "run_and_clean",
]

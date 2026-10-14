from typing import Literal, get_args
import shutil
import os
import subprocess
from pathlib import Path
import tempfile
import importlib.resources

import attrs
import mdtraj

Topology = Literal["in", "out"]
TOPOLOGYS = frozenset(get_args(Topology))
KEEP_HETEROGENS = {
    True: "1",
    False: "0",
}

@attrs.define
class ImmersPlainOutput:
    output_pdb: Path
    datapar_file: Path
    datasub_file: Path

def run_wrapped_immers_plain(
        input_pdb: Path,
        output_dir: Path,
        topology: Topology,
        keep_heterogens: bool,
) -> ImmersPlainOutput:

    if topology not in TOPOLOGYS:
        raise ValueError(f"Invalid topology spec: {topology}")

    # add a space for fixed width columns
    elif topology == "in":
        topology = "in "

    _keep_heterogens = KEEP_HETEROGENS[keep_heterogens]

    with tempfile.TemporaryDirectory("immers-plain") as tmp_dir:
        tmp_dir = Path(tmp_dir)

        tmp_dir = tmp_dir.resolve()

        # link in the input PDB
        _input_pdb = tmp_dir / "aaaa.pdb"

        shutil.copy2(input_pdb, _input_pdb)


        # generate the input file
        line = f" {_keep_heterogens} {topology} {_input_pdb.name}\n"

        input_spec_file = tmp_dir / "input.inp"
        input_spec_file.write_text(line)


        # link in the res.lib
        reslib = importlib.resources.files("ppm2._pkg_data") / "res.lib"
        (tmp_dir / "res.lib").symlink_to(reslib)

        # then run the executable
        exe = importlib.resources.files("ppm2._bin") / "immers"
        with open(input_spec_file, 'r') as input_stream:
            result = subprocess.run(
                [exe],
                cwd=tmp_dir,
                stdin=input_stream,
                capture_output=True,
            )

        if result.returncode != 0:
            raise RuntimeError(
                f"immers executable failed with code '{result.returncode}'. \n"
                f"stdout: {result.stdout.decode} \n"
                f"stderr: {result.stderr.decode}"
            )

        # then collect the outputs
        shutil.move(
            input_spec_file,
            output_dir / "input.inp",
        )

        tmp_output_pdb_path = tmp_dir / "aaaaout.pdb"
        output_pdb_path = output_dir / "output.pdb"
        shutil.move(
            tmp_output_pdb_path,
            output_pdb_path,
        )

        tmp_datapar_path = tmp_dir / "datapar1"
        output_datapar_path = output_dir / "datapar1"
        shutil.move(
            tmp_datapar_path,
            output_datapar_path,
        )

        tmp_datasub_path = tmp_dir / "datasub1"
        output_datasub_path = output_dir / "datasub1"
        shutil.move(
            tmp_datasub_path,
            output_datasub_path,
        )

        return ImmersPlainOutput(
            output_pdb=output_pdb_path,
            datapar_file=output_datapar_path,
            datasub_file=output_datasub_path,
        )


@attrs.define
class MembraneZ:
    """Hydrophobic slab along z in the oriented PPM frame, in angstroms.

    After immers orientation the bilayer midplane is z=0 and the membrane
    normal is +z. Dummy N atoms sit on `lower`, dummy O atoms on `upper`.
    `hydrophobic_depth` is not used: that is a protein insertion statistic,
    not a plane location.
    """
    midplane: float
    lower: float
    upper: float
    half_thickness: float

    def contains(self, z: float) -> bool:
        """True if z is inside the hydrophobic core, inclusive of the planes."""
        return self.lower <= z <= self.upper


@attrs.define
class PlacementData:
    # in angstroms
    hydrophobic_thickness: float
    hydrophobic_depth: float
    # degrees
    tilt_angle: float
    tilt_angle_err: float
    # in kcal/mol
    transfer_energy: float

    def membrane_z(self) -> MembraneZ:
        half = self.hydrophobic_thickness / 2.0
        return MembraneZ(
            midplane=0.0,
            lower=-half,
            upper=half,
            half_thickness=half,
        )

@attrs.define
class SubunitSegment:
    index: int
    start_res_idx: int
    end_res_idx: int

@attrs.define
class Subunit:
    name: str
    tilt_angle: float
    regions: list[SubunitSegment]
    
@attrs.define
class TransmembraneRegions:
    subunits: dict[str, Subunit]
    
@attrs.define
class ImmersOutput:
    output_pdb: Path
    placement: PlacementData
    transmembrane_regions: TransmembraneRegions

@attrs.define
class PPMReport:
    placement: PlacementData
    transmembrane_regions: TransmembraneRegions
    membrane_z: MembraneZ

def parse_datapar(f: Path) -> PlacementData:
    text = f.read_text()

    entries = [entry.strip() for entry in text.split(";")]

    return PlacementData(
        hydrophobic_thickness=float(entries[1]),
        hydrophobic_depth=float(entries[2]),
        tilt_angle=float(entries[3]),
        tilt_angle_err=float(entries[4]),
        transfer_energy=float(entries[5]),
    )

def parse_datasub(f: Path):

    text = f.read_text()

    subunits = {}
    for line in text.splitlines():

        entries = [entry.strip() for entry in text.split(";")]

        subunit_name = entries[1]

        segment_entries = [entry.strip() for entry in entries[3].split(",")]
        segments = []
        for segment_string in segment_entries:

            seg_idx_str, rest = segment_string.split("(")
            start_idx, end_idx = [int(e.strip()) for e in rest.strip(")").strip().split("-")]

            segments.append(
                SubunitSegment(
                    index=int(seg_idx_str),
                    start_res_idx=start_idx,
                    end_res_idx=end_idx,
                )
            )

        subunits[subunit_name] = Subunit(
                name=subunit_name,
                tilt_angle=float(entries[2]),
                regions=segments,
            )

    return TransmembraneRegions(
        subunits=subunits,
    )


def run_wrapped_immers(
        input_pdb: Path,
        output_pdb: Path,
        topology: Topology,
        keep_heterogens: bool,
) -> ImmersOutput:

    with tempfile.TemporaryDirectory("immers-extract") as tmp_dir:
        tmp_dir = Path(tmp_dir)

        plain_output = run_wrapped_immers_plain(
            input_pdb=input_pdb,
            output_dir=tmp_dir,
            topology=topology,
            keep_heterogens=keep_heterogens,
        )

        # parse the par and sub files
        placement_data = parse_datapar(plain_output.datapar_file)
        tm_data = parse_datasub(plain_output.datasub_file)

        # move the PDB
        shutil.move(
            plain_output.output_pdb,
            output_pdb,
        )

        return ImmersOutput(
            output_pdb=output_pdb,
            placement=placement_data,
            transmembrane_regions=tm_data,
        )

def _clean_immers_pdb(
        input_pdb: Path,
) -> mdtraj.Trajectory:

    in_traj = mdtraj.load(str(input_pdb))
    # remove dummy atoms
    protein_only_traj = in_traj.atom_slice(in_traj.topology.select("not resname DUM"))

    return protein_only_traj
    
def run_and_clean(
        input_pdb: Path,
        output_pdb: Path,
        topology: Topology,
        keep_heterogens: bool,
) -> PPMReport:

    
    with tempfile.TemporaryDirectory("immers-extract") as tmp_dir:
        tmp_dir = Path(tmp_dir)

        plain_output = run_wrapped_immers_plain(
            input_pdb=input_pdb,
            output_dir=tmp_dir,
            topology=topology,
            keep_heterogens=keep_heterogens,
        )

        # parse the par and sub files
        placement_data = parse_datapar(plain_output.datapar_file)
        tm_data = parse_datasub(plain_output.datasub_file)

        clean_traj = _clean_immers_pdb(plain_output.output_pdb)
        clean_traj.save(output_pdb)

        membrane_z = placement_data.membrane_z()

        return PPMReport(
            placement=placement_data,
            transmembrane_regions=tm_data,
            membrane_z=membrane_z,
        )

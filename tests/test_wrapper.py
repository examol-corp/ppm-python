import ppm2
from ppm2.wrapper import run_wrapped_immers_plain, parse_datapar, parse_datasub, run_wrapped_immers, PlacementData, Subunit, TransmembraneRegions, SubunitSegment

def test_run_wrapped_immers(test_data, tmp_path):

    with test_data("1rsy.pdb") as input_pdb:
        output = run_wrapped_immers_plain(
            input_pdb=input_pdb,
            output_dir=tmp_path,
            topology="in",
            keep_heterogens=False,
        )

    assert output.output_pdb.exists()
    assert output.datapar_file.exists()
    assert output.datasub_file.exists()

    
    with test_data("1gzm.pdb") as input_pdb:
        assert run_wrapped_immers_plain(
            input_pdb=input_pdb,
            output_dir=tmp_path,
            topology="out",
            keep_heterogens=False,
        )
    

    assert output.output_pdb.exists()
    assert output.datapar_file.exists()
    assert output.datasub_file.exists()
    

def test_parse_datapar(test_data):

    with test_data("datapar1") as datapar_path:

        assert parse_datapar(datapar_path) == PlacementData(
        hydrophobic_thickness=2.6,
        hydrophobic_depth=10.0,
        tilt_angle=23,
        tilt_angle_err=19,
        transfer_energy=-4.4,
    )

def test_parse_datasub(test_data):

    with test_data("datasub1") as datasub_path:

        assert parse_datasub(datasub_path) == TransmembraneRegions(
        subunits={
            "A" : Subunit(
                name="A",
                tilt_angle=11.,
                regions=[
                    SubunitSegment(
                        index=1,
                        start_res_idx=35,
                        end_res_idx=60,
                    ),
                    SubunitSegment(
                        index=2,
                        start_res_idx=72,
                        end_res_idx=99,
                    ),
                    SubunitSegment(
                        index=3,
                        start_res_idx=109,
                        end_res_idx=133,
                    ),
                    SubunitSegment(
                        index=4,
                        start_res_idx=151,
                        end_res_idx=173,
                    ),
                    SubunitSegment(
                        index=5,
                        start_res_idx=202,
                        end_res_idx=224,
                    ),
                    SubunitSegment(
                        index=6,
                        start_res_idx=253,
                        end_res_idx=277,
                    ),
                    SubunitSegment(
                        index=7,
                        start_res_idx=286,
                        end_res_idx=308,
                    ),
                ],
            )
        }
    )
        
def test_run_wrapped_immers(test_data, tmp_path):

    with test_data("1rsy.pdb") as input_pdb:
        output = run_wrapped_immers(
            input_pdb=input_pdb,
            output_pdb=(tmp_path / "out.pdb"),
            topology="in",
            keep_heterogens=False,
        )

    assert output.output_pdb.exists()

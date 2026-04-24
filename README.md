
# PPM Python: Positioning of Proteins in Membranes Python Wrapper

Python installable package for the set of `ppm` tools for orientation
and placement of membrane proteins in lipid membranes.

For a description of the method see: https://doi.org/10.1093/nar/gkr703

This is a derivative work from the PPM 2 code from this
repository: https://cggit.cc.lehigh.edu/biomembhub/ppm2_server_code
from the BioMembHub.

The goal is to have a python packaged version of the software with
some light wrappers around it to make it easier to use.

## Installation

```console
pip install git+https://github.com/examol-corp/ppm2.git
```

## Usage

In PPM2 and PPM3 the executable is named `immers` in both. Wheel
builds of this project disambiguate this with `immers2` for PPM2 and
`immers3` for PPM3. These are the exact executables provided by the
original project.

(PPM3 is not implemented in this repo yet.)

To use the wrapper CLIs see the names `ppm2` and `ppm3`.

Note that to use the original `immers2` CLI you will need a copy of
the `res.lib` file in your current working directory, which can be
found at `src/ppm2/_pkg_data/res.lib`.

### Examples

#### Raw immers executable

Run the raw bundled executable:

```console
cd tests/examples/testA
immers2 < input.inp
cd -
```

Note that you need to have a `res.lib` file in the cwd when executing.

#### Wrapped Executor CLI

```console
  ppm2 run \
    tests/examples/test-wrapped-cli/integral/input/1gzm.pdb \
    tests/examples/test-wrapped-cli/integral/output/1gzm_oriented.pdb \
    --topology in > tests/examples/test-wrapped-cli/integral/output/1gzm.ppm_report.json
```

This outputs the PDB to your desired location and the other metadata
that would come out have been parsed and transformed into the JSON
output on stdout.

#### Python Library

```python
from pathlib import Path
import ppm2

output = ppm2.run_wrapped_immers(
    input_pdb=Path("path/to/my.pdb"),
    output_pdb=Path("path/to/oriented.pdb"),
    topology="in",
    keep_heterogens=False,
)

# the path to the output pdb
output.output_pdb.exists()

# the placement data (thickness, tilt angle etc.)
output.placement

# the transmembrane regions identified in the protein
output.transmembrane_regions
```


## Contributing

```console
just build
just test
just test-cli
```

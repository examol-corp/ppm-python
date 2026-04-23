
# PPM: Placement of Proteins in Membranes

This is a derivative work from the PPM 2 code from this
repository: https://cggit.cc.lehigh.edu/biomembhub/ppm2_server_code
from the BioMembHub.

The goal is to have a python packaged version of the software with
some light wrappers around it to make it easier to use.

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


## Contributing

```
just build
just test
```

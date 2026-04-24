"""CLI wrapper for immers.

immers needs the res.lib file which we don't want to have to guarantee
is in the same directory so we provide a wrapper that can create a
temporary directory to symlink in the res.lib and then generate
outputs in a more controlled way.

"""
from typing import Annotated
from pathlib import Path
import sys
import cyclopts

import cattrs
from cattrs.preconf.json import make_converter

from .wrapper import run_wrapped_immers, Topology

JSON_CONVERTER = make_converter()

app = cyclopts.App()


@app.command()
def run(
        input: Annotated[
            Path,
            cyclopts.Parameter(
                validator=cyclopts.validators.Path(
                    exists=True,
                    dir_okay=False,
                ),
            ),
        ],
        output: Annotated[
            Path,
            cyclopts.Parameter(
                validator=cyclopts.validators.Path(
                    exists=False,
                    dir_okay=False,
                ),
            ),
        ],
        topology: Topology,
        keep_heterogens: bool = False,
):

    output = run_wrapped_immers(
        input_pdb=input,
        output_pdb=output,
        topology=topology,
        keep_heterogens=keep_heterogens,
    )

    sys.stdout.write(JSON_CONVERTER.dumps(output))

if __name__ == "__main__":
    app()

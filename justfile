
build:
    uvx --from build pyproject-build --wheel -Cbuild-dir=build

test: build
    python -m venv .test-venv && cd tests/examples/testA/ && immers2 < test.inp


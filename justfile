
build:
    rm -rf dist
    uvx --from build pyproject-build --wheel -Cbuild-dir=build

venv:
    rm -rf .test-venv && python -m venv .test-venv && source ./.test-venv/bin/activate && pip install dist/ppm2-*.whl && pip install pytest && deactivate

test: build venv
    source ./.test-venv/bin/activate && pytest -vv tests/

test-cli: build venv
    # raw
    cd tests/examples/testA
    source ./.test-venv/bin/activate && immers2 < test.inp
    cd -
    
    # wrapped
    source ./.test-venv/bin/activate && \
        ppm2 run \
            tests/examples/test-wrapped-cli/integral/input/1gzm.pdb \
            tests/examples/test-wrapped-cli/integral/output/1gzm_oriented.pdb \
            --topology in > tests/examples/test-wrapped-cli/integral/output/1gzm.ppm_report.json
    source ./.test-venv/bin/activate && \
        ppm2 run \
            tests/examples/test-wrapped-cli/peripheral/input/1rsy.pdb \
            tests/examples/test-wrapped-cli/peripheral/output/1rsy_oriented.pdb \
            --topology out > tests/examples/test-wrapped-cli/peripheral/output/1rsy.ppm_report.json

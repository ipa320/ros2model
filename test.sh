#!/bin/bash
COVERAGE=${1-$COVERAGE}

function log_error {
    local out; out=$(mktemp)
    # shellcheck disable=SC2216
    # shellcheck disable=SC2260
    "$@" &> "$out" | true # '|| err=$?' disables errexit
    local err=${PIPESTATUS[0]}
    if [ "$err" -ne "${EXPECT-0}" ]; then
        cat "$out"
        echo "'$*' failed with $err (expected: ${EXPECT-0})"
        rm -rf "$out"
        exit "$err"
    fi
    rm -rf "$out"
}

function run_python {
    if [ "$COVERAGE" != true ]; then
        log_error venv/*/python "$@"
    else
        log_error venv/*/coverage run -p --source=. "$@"
    fi
}

if [ "$COVERAGE" = true ]; then
    venv/*/pip install coverage
    rm -rf .coverage* htmlcov
fi

# clean up tmp
rm -rf test/tmp
export DMSE_CACHE=test/tmp/cache

# run unit test
run_python -m unittest discover -s test/unittest/

if [ "$COVERAGE" = true ]; then
    venv/*/coverage combine
    venv/*/coverage report
    rm -rf .coverage.* htmlcov
    venv/*/coverage html
fi

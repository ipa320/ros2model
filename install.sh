#!/bin/bash
set -euo pipefail

if [ ! -d venv ]; then
    for p in "py -3.8" "py -3" "python3.8" "python3" "python"; do
        if $p -V &>/dev/null; then
            pycmd=$p
            break
        fi
    done
    ${pycmd:?Could not determine python executable} -m venv venv
fi

shopt -s nullglob
pip_candidates=(venv/bin/pip venv/*/pip)
pip_cmd=""
for candidate in "${pip_candidates[@]}"; do
    if [ -x "$candidate" ]; then
        pip_cmd="$candidate"
        break
    fi
done
shopt -u nullglob

if [ -z "$pip_cmd" ]; then
    echo "Could not locate pip inside the virtual environment." >&2
    exit 1
fi

extra_args=()
if [ -d wheels ] && compgen -G "wheels/*" > /dev/null; then
    extra_args=(--find-links wheels)
fi

if [ "${GIT_ACTION:-false}" = true ]; then
    "$pip_cmd" install -e .
    if [ "${#extra_args[@]}" -gt 0 ]; then
        "$pip_cmd" install "${extra_args[@]}" -e .
    fi
else
    "$pip_cmd" install -e src/ros2model
    if [ "${#extra_args[@]}" -gt 0 ]; then
        "$pip_cmd" install "${extra_args[@]}" -e src/ros2model
    fi
fi

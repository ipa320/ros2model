#!/bin/bash

if [ ! -d venv ]; then
    for p in "py -3.8" "py -3" "python3.8" "python3" "python"; do
        if $p -V &>/dev/null; then
            pycmd=$p
            break
        fi
    done
    ${pycmd:?Could not determine python executable} -m venv venv
fi

venv/*/pip install -e src/ros2model

venv/*/pip install --find-links wheels -e src/ros2model

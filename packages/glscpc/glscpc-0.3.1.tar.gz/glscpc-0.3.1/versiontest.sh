#!/bin/bash

# Script for locally testing all supported python versions.
# This is a hack that makes many assumptions, but is good enough for manual testing.

set -e

SCRIPT="set -e
$(yq -r '.test.script | join("\n")' .gitlab-ci.yml)"

function run_version() {
    PY_VERSION=$1
    figlet -f small "Testing $PY_VERSION"
    docker run -i --rm --name "glscpc-$PY_VERSION" --mount "type=bind,source=$(pwd),destination=/app,readonly=true" --workdir /app --entrypoint bash "python:$PY_VERSION" <<< "$SCRIPT"
    echo "$PY_VERSION OK"
}

hatch build --clean
# Intentional unquoted subshell: split on space.
for PY_VERSION in $(yq -r '.test.parallel.matrix[0].PY_VERSION | join(" ")' .gitlab-ci.yml); do
     run_version "$PY_VERSION"
done

figlet -f small "Success!"

#!/bin/bash

SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TOP_DIR=${SCRIPTS_DIR}/..

# Get the most recent annotated tag
VERSION=$(git describe --abbrev=0 --tags)
TAG_NAME=$(basename `git rev-parse --show-toplevel`)

echo "Building image ${TAG_NAME}:${VERSION}"
docker build --tag tobiaslocker/${TAG_NAME}:${VERSION} -f Dockerfile ${TOP_DIR}

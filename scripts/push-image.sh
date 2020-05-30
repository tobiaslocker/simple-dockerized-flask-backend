#!/bin/bash

PROJECT_ID="quant-signals"

# Get the most recent annotated tag
VERSION=$(git describe --abbrev=0 --tags)
TAG_NAME=$(basename `git rev-parse --show-toplevel`)

echo "Building image ${TAG_NAME}:${VERSION}"
docker push gcr.io/${PROJECT_ID}/${TAG_NAME}:${VERSION}

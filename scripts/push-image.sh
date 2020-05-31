#!/bin/bash

# Get the most recent annotated tag
VERSION=$(git describe --abbrev=0 --tags)
TAG_NAME=$(basename `git rev-parse --show-toplevel`)

echo "Pushing image tobiaslocker/${TAG_NAME}:${VERSION}"

docker push tobiaslocker/${TAG_NAME}:${VERSION}

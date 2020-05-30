#!/bin/bash
# Get the most recent annotated tag
VERSION=$(git describe --abbrev=0 --tags)
TAG_NAME=$(basename `git rev-parse --show-toplevel`)
docker run  -it --rm -p 8080:8080 ${TAG_NAME}:${VERSION}

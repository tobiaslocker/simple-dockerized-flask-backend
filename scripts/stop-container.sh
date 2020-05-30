#!/bin/bash
# Get the most recent annotated tag
VERSION=$(git describe --abbrev=0 --tags)
TAG_NAME=$(basename `git rev-parse --show-toplevel`)




docker stop $(docker ps -a -q --filter ancestor=${TAG_NAME}:${VERSION} --format="{{.ID}}")


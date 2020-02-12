#!/bin/bash

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

if [[ -z "${TRAVIS_TAG}" ]]; then
docker build . -t dinutac/estuary-viewer:"${TRAVIS_TAG}"
docker push dinutac/estuary-viewer:"${TRAVIS_TAG}"
else
docker build . -t dinutac/estuary-viewer:latest
docker push dinutac/estuary-viewer:latest
fi
#!/bin/bash

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

if [[ -z "${TRAVIS_TAG}" ]]; then
#alpine
docker build . -t dinutac/estuary-testrunner:"${TRAVIS_TAG}"
docker push dinutac/estuary-testrunner:"${TRAVIS_TAG}"
#centos
docker build . -t dinutac/estuary-testrunner-centos:"${TRAVIS_TAG}"
docker push dinutac/estuary-testrunner-centos:"${TRAVIS_TAG}"
else
#alpine
docker build . -t dinutac/estuary-testrunner:latest
docker push dinutac/estuary-testrunner:latest
#centos
docker build -t dinutac/estuary-testrunner-centos:latest -f Dockerfiles/Dockerfile_centos .
docker push dinutac/estuary-testrunner-centos:latest
fi
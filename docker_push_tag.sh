#!/bin/bash

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

#alpine
docker build . -t dinutac/estuary-testrunner:"${TRAVIS_TAG}"
docker push dinutac/estuary-testrunner:"${TRAVIS_TAG}"

#centos
docker build -t dinutac/estuary-testrunner-centos:"${TRAVIS_TAG}" -f Dockerfiles/Dockerfile_centos .
docker push dinutac/estuary-testrunner-centos:"${TRAVIS_TAG}"

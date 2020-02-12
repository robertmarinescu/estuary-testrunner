#!/bin/bash

echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

#alpine
docker build . -t dinutac/estuary-testrunner:latest
docker push dinutac/estuary-testrunner:latest

#centos
docker build -t dinutac/estuary-testrunner-centos:latest -f Dockerfiles/Dockerfile_centos .
docker push dinutac/estuary-testrunner-centos:latest

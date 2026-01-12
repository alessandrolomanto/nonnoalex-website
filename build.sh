#!/bin/bash

echo "Insert build version:"
read version

echo "Preparing build: $version";
docker build -t nonnoalex-website:$version .
docker tag nonnoalex-website:$version docker.nonnoalex.dev/nonnoalex/nonnoalex-website:$version
docker push docker.nonnoalex.dev/nonnoalex/nonnoalex-website:$version

exit 0

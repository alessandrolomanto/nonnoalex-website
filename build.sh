#!/bin/bash

echo "Insert build version:"
read version

echo "Preparing build: $version";
docker build -t nonnoalex-website:$version .
docker tag nonnoalex-website:$version localhost:5000/nonnoalex-website:$version
docker push localhost:5000/nonnoalex-website:$version

exit 0


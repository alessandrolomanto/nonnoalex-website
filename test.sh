#!/usr/bin/env bash
set -euo pipefail

image="nonnoalex-website:test"
container="nonnoalex-website-test-$$"

cleanup() {
  docker rm -f "$container" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker build -t "$image" .
docker run -d --name "$container" -p 127.0.0.1::80 "$image" >/dev/null
port="$(docker port "$container" 80/tcp | sed 's/.*://')"

python3 test/site_test.py "http://127.0.0.1:$port"

helm lint ./helm/nonnoalex-website
helm template nonnoalex-website ./helm/nonnoalex-website | grep -q 'image: "docker.nonnoalex.dev/nonnoalex/nonnoalex-website:1.0.7"'
helm template nonnoalex-website ./helm/nonnoalex-website \
  --set-string image.tag=release-test | grep -q 'image: "docker.nonnoalex.dev/nonnoalex/nonnoalex-website:release-test"'

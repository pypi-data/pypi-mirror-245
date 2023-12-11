#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p
gitlabci-local -n none -p
DOCKER_HOST=tcp://0.0.0.0:9999 gitlabci-local -E d -p && exit 1 || true
gitlabci-local -E auto -p
CI_LOCAL_ENGINE=docker,podman,auto gitlabci-local -p
gitlabci-local -E '' -p
PODMAN_BINARY_PATH=podman-missing gitlabci-local -E podman -p && exit 1 || true
PODMAN_BINARY_PATH=ls gitlabci-local -E podman -p && exit 1 || true

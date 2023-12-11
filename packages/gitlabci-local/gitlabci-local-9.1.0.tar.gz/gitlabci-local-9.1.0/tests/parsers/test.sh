#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -c ./.gitlab-ci.corrupt.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.configurations.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.script.yml -p && exit 1 || true
gitlabci-local -c /sys/bus/gpio/uevent -p && exit 1 || true

#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p && exit 1 || true
gitlabci-local --display -p || echo 'Display: Support for DISPLAY in CI tests is incomplete...'
gitlabci-local -c ./.gitlab-ci.local.yml -p || echo 'Display: Support for DISPLAY in CI tests is incomplete...'

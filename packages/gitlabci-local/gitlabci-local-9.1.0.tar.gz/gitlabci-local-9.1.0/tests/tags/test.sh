#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p
gitlabci-local -m -p && exit 1 || true
gitlabci-local -t upload -p && exit 1 || true
gitlabci-local -t publish -p
gitlabci-local -t deploy,publish -p
gitlabci-local -t deploy,local,publish -p
gitlabci-local 'Job 3'
gitlabci-local -p three && exit 1 || true
gitlabci-local -m -p three

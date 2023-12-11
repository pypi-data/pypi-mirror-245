#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p && exit 1 || true
gitlabci-local 'Job 1' 'Job 2'
gitlabci-local -H -p && exit 1 || true
gitlabci-local -H 'Job 1' 'Job 2'
PYTHONIOENCODING=ascii gitlabci-local -H -p && exit 1 || true
PYTHONIOENCODING=ascii gitlabci-local -H 'Job 1' 'Job 2'

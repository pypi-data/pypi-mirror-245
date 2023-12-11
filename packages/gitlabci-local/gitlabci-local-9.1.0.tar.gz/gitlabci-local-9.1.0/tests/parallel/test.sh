#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Drop validation environment
unset PYTHON_VERSION

# Run tests
gitlabci-local 'Job 1'
gitlabci-local -e PYTHON_VERSION=3.6 'Job 1'
gitlabci-local -e PYTHON_VERSION=0.0 'Job 1' && exit 1 || true
gitlabci-local -H 'Job 2'
gitlabci-local -H -e VALUE1= 'Job 2' && exit 1 || true
gitlabci-local -H -e VALUE1=3 'Job 2'
gitlabci-local -H -e VALUE1=4 'Job 2' && exit 1 || true
gitlabci-local -H -e VALUE2= 'Job 2' && exit 1 || true
gitlabci-local -H -e VALUE2=2 'Job 2'
gitlabci-local -H -e VALUE2=3 'Job 2' && exit 1 || true
gitlabci-local -H 'Job 2: [3.6, 1, 1]'
gitlabci-local -H -e VALUE2=2 'Job 2: [3.6, 1, 1]' && exit 1 || true
gitlabci-local -H 'Job 2: [3.6, 1, 2]'
gitlabci-local -H 'Job 2: [3.6, 1, 3]' && exit 1 || true
gitlabci-local 'Job 3'

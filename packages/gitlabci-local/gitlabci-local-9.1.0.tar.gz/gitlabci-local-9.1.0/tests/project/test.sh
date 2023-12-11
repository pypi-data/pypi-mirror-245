#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p
gitlabci-local -H -p
gitlabci-local 'Job 2' && exit 1 || true
gitlabci-local -e CI_VARIABLE_DIR=. 'Job 2'
CI_VARIABLE_DIR=. gitlabci-local 'Job 2' && exit 1 || true
CI_VARIABLE_DIR=. gitlabci-local -e CI_VARIABLE_DIR 'Job 2'
gitlabci-local 'Job 3'
gitlabci-local 'Job 4'
gitlabci-local -e CI_CONSTANT_PRE_DIR=. -e CI_CONSTANT_POST_DIR=. 'Job 3'

#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -h
gitlabci-local -c unknown/.gitlab-ci.yml && exit 1 || true
gitlabci-local -c ../../examples/ -d
gitlabci-local -c ../../examples/.gitlab-ci.yml -d
gitlabci-local -c ../../examples/.gitlab-ci.yml -d 'Job 1 - 1'
gitlabci-local -c ../../examples/.gitlab-ci.yml -d -i 'job 1 - 1'
gitlabci-local -c ../../examples/.gitlab-ci.yml --no-verbose 'Job 1 - 1'
gitlabci-local -c ../../examples/.gitlab-ci.yml --quiet 'Job 1 - 1'
gitlabci-local -c ../../examples/.gitlab-ci.yml --no-verbose --quiet 'Job 1 - 1'

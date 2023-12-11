#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local --pull
gitlabci-local -d
gitlabci-local -p
gitlabci-local -c ./.gitlab-ci.local.yml -p
gitlabci-local -c ./.gitlab-ci.name.yml -p
gitlabci-local -c ./.gitlab-ci.simple.yml -p
gitlabci-local -c ./.gitlab-ci.local.entrypoint.yml -p

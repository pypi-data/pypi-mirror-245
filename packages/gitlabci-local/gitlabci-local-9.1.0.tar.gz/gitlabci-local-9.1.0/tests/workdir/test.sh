#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -c ./.gitlab-ci.builds.yml -p
gitlabci-local -c ./.gitlab-ci.host.yml -p -r
gitlabci-local -c ./.gitlab-ci.clone.yml -p
gitlabci-local -c ./.gitlab-ci.clone.yml -p -r && exit 1 || true

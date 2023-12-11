#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -H -p
gitlabci-local -c ./.gitlab-ci.incomplete.yml -H 'Job 1'
gitlabci-local -c ./.gitlab-ci.incomplete.yml -H 'Job 2'
gitlabci-local -c ./.gitlab-ci.incomplete.yml -H 'Job 3' && exit 1 || true
gitlabci-local -c ./.gitlab-ci.partial.yml -H -p
gitlabci-local -c ./.gitlab-ci.partial.yml -H 'Job 3' && exit 1 || true
gitlabci-local -c ./.gitlab-ci.partial.yml -H 'Job 4' && exit 1 || true
gitlabci-local -c ./.gitlab-ci.stages.yml -H -p

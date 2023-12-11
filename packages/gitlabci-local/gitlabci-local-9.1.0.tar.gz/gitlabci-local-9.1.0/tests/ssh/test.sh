#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Prepare paths
mkdir -p ~/.ssh

# Run tests
timeout 5 gitlabci-local 'Job 1' --ssh
gitlabci-local --ssh 'Job 1' </dev/null && exit 1 || true
gitlabci-local --ssh -e OTHER=argument 'Job 1'
gitlabci-local --ssh -p
timeout 5 gitlabci-local --ssh root 'Job 1'
timeout 5 gitlabci-local -c ./.gitlab-ci.user.yml --ssh user 'Job 1'
timeout 5 gitlabci-local -c ./.gitlab-ci.user.yml --ssh user -p
timeout 5 gitlabci-local -c ./.gitlab-ci.local.bool.yml 'Job 1'
timeout 5 gitlabci-local -c ./.gitlab-ci.local.root.yml 'Job 1'
timeout 5 gitlabci-local -c ./.gitlab-ci.local.user.yml 'Job 1'
timeout 5 gitlabci-local -c ./.gitlab-ci.local.user.yml --ssh other 'Job 1' && exit 1 || true
timeout 5 gitlabci-local -c ./.gitlab-ci.local.user.yml --ssh user 'Job 1'

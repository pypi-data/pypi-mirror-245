#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -c ./.gitlab-ci.yml --dump | grep 'image: local'
gitlabci-local -c ./.gitlab-ci.yml --dump | grep 'services:'
gitlabci-local -c ./.gitlab-ci.yml -p
gitlabci-local -c ./.gitlab-ci.conflict.after.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.conflict.before.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.conflict.image.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.conflict.services.yml -p && exit 1 || true

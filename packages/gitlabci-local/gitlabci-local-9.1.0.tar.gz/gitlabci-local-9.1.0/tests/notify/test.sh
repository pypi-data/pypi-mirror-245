#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local --notify 'Job 1'
gitlabci-local --notify 'Job 2' && exit 1 || true
gitlabci-local --notify -p && exit 1 || true
NOTIFY_BINARY_PATH='echo' gitlabci-local --notify -p && exit 1 || true
NOTIFY_BINARY_PATH='notify-missing' gitlabci-local --notify -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.local.yml 'Job 1'
gitlabci-local -c ./.gitlab-ci.local.yml 'Job 2' && exit 1 || true
gitlabci-local -c ./.gitlab-ci.local.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.image.yml --pull
timeout 10 timeout -k 8 5 gitlabci-local -c ./.gitlab-ci.image.yml --bash --notify 'Job 1' && exit 1 || true
timeout 10 timeout -k 8 5 gitlabci-local -c ./.gitlab-ci.image.yml --debug --notify 'Job 1' && exit 1 || true
timeout 5 gitlabci-local -c ./.gitlab-ci.image.yml --notify 'Job 2' && exit 1 || true

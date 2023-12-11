#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local unknown_job && exit 1 || true
gitlabci-local -p unknown_stage && exit 1 || true
gitlabci-local -p && exit 1 || true
gitlabci-local -p one two
gitlabci-local -s -p one two </dev/null
gitlabci-local -c ./.gitlab-ci.defaults.yml --dump
gitlabci-local -c ./.gitlab-ci.defaults.yml -p
gitlabci-local -c ./.gitlab-ci.test.yml -p
gitlabci-local -c ./.gitlab-ci.unknown.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.disabled.yml -p
gitlabci-local -c ./.gitlab-ci.pre.post.explicit.yml -p
gitlabci-local -c ./.gitlab-ci.pre.post.implicit.yml -p

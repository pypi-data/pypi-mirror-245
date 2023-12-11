#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local --pull
gitlabci-local --pull
gitlabci-local --pull 'Job 4'
gitlabci-local --pull 'Job 3' && exit 1 || true
gitlabci-local --pull -p containers
gitlabci-local --pull -p native  && exit 1 || true
gitlabci-local --pull --force
pexpect-executor -- gitlabci-local --pull --force
gitlabci-local --rmi
gitlabci-local --rmi
gitlabci-local -p
gitlabci-local -c ./.gitlab-ci.default.yml --dump
CI_LOCAL_IMAGE_DEFAULT=registry.gitlab.com/adriandc/gitlabci-local/ruby:3.1 gitlabci-local -c ./.gitlab-ci.default.yml --pull
CI_LOCAL_IMAGE_DEFAULT=registry.gitlab.com/adriandc/gitlabci-local/ruby:3.1 gitlabci-local -c ./.gitlab-ci.default.yml -p
CI_LOCAL_IMAGE_DEFAULT=registry.gitlab.com/adriandc/gitlabci-local/ruby:3.1 gitlabci-local -c ./.gitlab-ci.extends.yml -p

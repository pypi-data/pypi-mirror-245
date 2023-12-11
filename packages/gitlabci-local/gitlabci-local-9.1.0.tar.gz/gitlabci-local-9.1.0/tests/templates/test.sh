#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local 'Job 1' 'Job 2' 'Job 3'
gitlabci-local -B -A 'Job 1' 'Job 2' 'Job 3'
gitlabci-local -c ./.gitlab-ci.partial.yml -p
gitlabci-local --settings | grep '^no_script_fail = '
gitlabci-local --no-script-fail -c ./.gitlab-ci.partial.yml -p && exit 1 || true
pexpect-executor --space --down --space --enter -- gitlabci-local -c ./.gitlab-ci.partial.yml
gitlabci-local -c ./.gitlab-ci.stages.yml -p template_stage_1
gitlabci-local -c ./.gitlab-ci.stages.yml -p template_stage_2
gitlabci-local -c ./.gitlab-ci.stages.yml -p template_stage_4

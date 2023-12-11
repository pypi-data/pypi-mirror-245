#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p && exit 1 || true
gitlabci-local 'Job 1'
gitlabci-local 'Job 2' && exit 1 || true
gitlabci-local 'Job 3' && exit 1 || true
gitlabci-local 'Job 4'
gitlabci-local 'Job 5' && exit 1 || true
gitlabci-local 'Job 6' && exit 1 || true
gitlabci-local 'Job 7'
gitlabci-local 'Job 8'
gitlabci-local 'Job 9'
gitlabci-local -c ./.gitlab-ci.incomplete.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.shebang.yml 'Job 1'
gitlabci-local -c ./.gitlab-ci.shebang.yml -e __GITLAB_CI_LOCAL_SHEBANG_MARKER_BASH__=true 'Job 1' && exit 1 || true
gitlabci-local -c ./.gitlab-ci.shebang.yml 'Job 2'
gitlabci-local -p --scripts

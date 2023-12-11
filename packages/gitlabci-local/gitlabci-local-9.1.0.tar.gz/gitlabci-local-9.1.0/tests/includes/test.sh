#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -c ./.gitlab-ci.default.yml -p
gitlabci-local -c ./.gitlab-ci.dict.yml -p
gitlabci-local -c ./.gitlab-ci.list.dict.yml -p
gitlabci-local -c ./.gitlab-ci.list.str.yml -p
gitlabci-local -c ./.gitlab-ci.local.yml -p
gitlabci-local -c ./.gitlab-ci.local.empty.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.nested.valid.yml -p
gitlabci-local -c ./.gitlab-ci.nested.missing.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.nested.loop.yml -p
gitlabci-local -c ./.gitlab-ci.project.yml -p
gitlabci-local -c ./.gitlab-ci.project.empty.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.project.missing.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.relative.faulty.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.relative.folder.yml -p
gitlabci-local -c ./.gitlab-ci.relative.root.yml -p
gitlabci-local -c ./.gitlab-ci.str.yml -p
gitlabci-local -c ./.gitlab-ci.variables.yml -p
gitlabci-local -c ./.gitlab-ci.wildcards.valid.yml -p
gitlabci-local -c ./.gitlab-ci.wildcards.local.missing.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.wildcards.project.missing.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.wildcards.recursive.faulty.yml -p && exit 1 || true
gitlabci-local -c ./.gitlab-ci.wildcards.recursive.missing.yml -p && exit 1 || true

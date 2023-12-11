#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local --settings
! type sudo >/dev/null 2>&1 || sudo -E env PYTHONPATH="${PYTHONPATH}" gitlabci-local --settings
gitlabci-local --set && exit 1 || true
gitlabci-local --set GROUP && exit 1 || true
gitlabci-local --set GROUP KEY && exit 1 || true
gitlabci-local --set package test 1
gitlabci-local --set package test 0
gitlabci-local --set package test UNSET
gitlabci-local --set updates enabled NaN
gitlabci-local --version
gitlabci-local --set updates enabled UNSET

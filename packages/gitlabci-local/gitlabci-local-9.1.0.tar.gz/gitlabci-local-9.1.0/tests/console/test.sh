#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
timeout 10 timeout -k 5 2 gitlabci-local --bash 'Job 1' </dev/null && exit 1 || true
timeout 10 timeout -k 5 2 gitlabci-local --bash 'Job 1' </dev/null && exit 1 || true
timeout 10 timeout -k 5 2 gitlabci-local --bash --no-console 'Job 1' && exit 1 || true
timeout 15 timeout -k 12 10 pexpect-executor --wait 2 --press exit --enter -- gitlabci-local --bash 'Job 1' && exit 1 || true
timeout 15 timeout -k 12 10 pexpect-executor -- timeout 3 gitlabci-local --bash --no-console 'Job 1' && exit 1 || true
timeout 10 timeout -k 5 2 gitlabci-local --bash 'Job 2' </dev/null && exit 1 || true
timeout --preserve-status 10 timeout --preserve-status -k 5 2 gitlabci-local --debug 'Job 1' </dev/null || {
  result=${?}
  test "${result}" -eq 143
}
timeout --preserve-status 10 timeout --preserve-status -k 5 2 gitlabci-local --debug 'Job 2' </dev/null && exit 1 || true

#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
CI_LOCAL_HISTORIES_DURATION_FAKE=0 gitlabci-local -p
CI_LOCAL_HISTORIES_DURATION_FAKE=10 gitlabci-local -p
CI_LOCAL_HISTORIES_DURATION_FAKE=62 gitlabci-local -p

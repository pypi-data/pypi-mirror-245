#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -H -p | cat
gitlabci-local -p | cat
gitlabci-local -p | head -n1
gitlabci-local -p | head -n4
gitlabci-local --dump | cat
gitlabci-local --dump | head -n10

#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -H -p
gitlabci-local -H -p --no-color
gitlabci-local --set themes no_color 1
gitlabci-local -H -p
gitlabci-local --set themes no_color 0
gitlabci-local -H -p
gitlabci-local --set themes no_color UNSET
gitlabci-local -H -p
FORCE_COLOR=1 gitlabci-local -H -p
FORCE_COLOR=0 gitlabci-local -H -p
NO_COLOR=1 gitlabci-local -H -p

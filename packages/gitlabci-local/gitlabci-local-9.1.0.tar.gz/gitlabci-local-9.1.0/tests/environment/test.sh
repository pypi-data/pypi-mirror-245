#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p
gitlabci-local -e USER -e VALUE_1=set1 -e VALUE_2=set2 -e VALUE_3=set3 -p
gitlabci-local -e FOLDER="$(readlink -f "${PWD}")" -v ./ 'Job 2'
gitlabci-local -e environment.env -p
VALUE_5=value_5 gitlabci-local -e environment.env -p
gitlabci-local -v ./:/opt 'Job 2'
gitlabci-local -v ./:/opt -w /opt/ 'Job 2'
gitlabci-local --dump | grep -A1 'services' | grep '\$'
gitlabci-local --dump -e environment.env | grep -A1 'services' | grep 'docker:dind'
IMAGE_REFERENCE_SERVICE=registry.gitlab.com/adriandc/gitlabci-local/docker:dind gitlabci-local --dump -e environment.env | grep -A1 'services' | grep 'docker:dind'

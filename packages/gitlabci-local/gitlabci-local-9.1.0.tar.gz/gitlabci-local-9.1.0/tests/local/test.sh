#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Prepare paths
mkdir -p ~/.ssh

# Run tests
gitlabci-local
gitlabci-local -p
gitlabci-local '1' && exit 1 || true
gitlabci-local 'Job 1'
gitlabci-local 'Job 9'
gitlabci-local -p local_first
gitlabci-local -n bridge 'Job 2' || (type podman >/dev/null 2>&1 && echo 'Podman engine: Network bridge may fail in GitLab CI containers')
CI_LOCAL_NETWORK=bridge gitlabci-local 'Job 2' || (type podman >/dev/null 2>&1 && echo 'Podman engine: Network bridge may fail in GitLab CI containers')
gitlabci-local -n host 'Job 2'
CI_LOCAL_NETWORK=host gitlabci-local 'Job 2'
gitlabci-local -n none 'Job 2'
CI_LOCAL_NETWORK=none gitlabci-local 'Job 2'
gitlabci-local 'Job 10'
gitlabci-local --host 'Job 10'

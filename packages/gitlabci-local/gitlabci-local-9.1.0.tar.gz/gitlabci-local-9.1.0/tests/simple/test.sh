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
gitlabci-local </dev/null && exit 1 || true
gitlabci-local -p
gitlabci-local -H --all </dev/null
gitlabci-local -H -q -p
gcil -H -p
timeout 5 gitlabci-local 'Job 1' -H --sockets
SSH_AUTH_SOCK=/tmp/ timeout 5 gitlabci-local 'Job 1' --ssh
timeout 10 timeout -k 8 5 gitlabci-local 'Job 1' --bash && exit 1 || true
timeout 10 timeout -k 8 5 gitlabci-local 'Job 2' --bash && exit 1 || true
timeout 10 timeout -k 8 5 gitlabci-local 'Job 1' --debug && exit 1 || true
timeout 10 timeout -k 8 5 gitlabci-local 'Job 1' --bash --shell 'bash --login' && exit 1 || true
! type sudo >/dev/null 2>&1 || (sudo -E env PYTHONPATH="${PYTHONPATH}" timeout 5 gitlabci-local 'Job 1' --debug && exit 1 || true)
gcil -H Job
gcil -H 1
gcil -H 4 && exit 1 || true
gcil -H -C 'set +x; echo "Overriding scripts commands"; echo "Succesful" && true' 'Job 2'
gcil -H -C 'set +x; echo "Overriding scripts commands"; echo "Failing" && false' 'Job 2' && exit 1 || true

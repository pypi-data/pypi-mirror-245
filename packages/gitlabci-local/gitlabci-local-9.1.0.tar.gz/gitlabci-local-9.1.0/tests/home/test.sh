#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests (.local)
gitlabci-local -c ./.gitlab-ci.env.yml -p
gitlabci-local -c ./.gitlab-ci.relative.yml -p
if [ "${OSTYPE}" = 'msys' ] || [ "${OSTYPE}" = 'win32' ]; then
  gitlabci-local -c ./.gitlab-ci.tilde.yml -p && exit 1 || true
  gitlabci-local -c ./.gitlab-ci.tilde.yml -p -w //root
else
  gitlabci-local -c ./.gitlab-ci.tilde.yml -p
fi

# Run tests (-v)
gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR="${HOME}" -v ~:~ -w ~ -p && exit 1 || true
if [ "${OSTYPE}" = 'msys' ] || [ "${OSTYPE}" = 'win32' ]; then
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR="${HOME}" -v ~://mnt -w ~ -p && exit 1 || true
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR='//root' -v ~://mnt -w //root -p
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR="${HOME}" -v "${HOME}"://mnt -w "${HOME}" -p && exit 1 || true
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR='//root' -v "${HOME}"://mnt -w //root -p
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR="${PWD}" -v "${PWD}"://mnt -w "${PWD}" -p && exit 1 || true
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR='//root' -v "${PWD}"://mnt -w //root -p
else
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR="${HOME}" -v ~:/mnt -w ~ -p
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR="${HOME}" -v "${HOME}:/mnt" -w "${HOME}" -p
  gitlabci-local -c ./.gitlab-ci.cli.yml -e WORKDIR="${PWD}" -v "${PWD}:/mnt" -w "${PWD}" -p || (type podman >/dev/null 2>&1 && echo 'Podman engine: CLI workdir is not created automatically as expected')
fi

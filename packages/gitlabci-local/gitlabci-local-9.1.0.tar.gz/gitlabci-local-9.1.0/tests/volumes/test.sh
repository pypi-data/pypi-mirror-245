#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Configure tests
set -ex

# Run tests
gitlabci-local -p
if [ "${OSTYPE}" = 'msys' ] || [ "${OSTYPE}" = 'win32' ]; then
  gitlabci-local -v ../../tests/volumes://opt/src:ro -p
  gitlabci-local -v ../../tests/volumes://opt/src:ro -v ../../tests/volumes://opt/src:ro -p
  gitlabci-local -v ../../tests/local://opt/src:ro -p
  gitlabci-local -v ../../tests/volumes://opt/src3:ro -p
  gitlabci-local -v ../../tests/local://opt/src:ro -v ../../tests/volumes://opt/src:ro -p && exit 1 || true
  gitlabci-local -w //opt/src -p
  gitlabci-local -w //opt/unknown -p
else
  gitlabci-local -v ../../tests/volumes:/opt/src:ro -p
  gitlabci-local -v ../../tests/volumes:/opt/src:ro -v ../../tests/volumes:/opt/src:ro -p
  gitlabci-local -v ../../tests/local:/opt/src:ro -p
  gitlabci-local -v ../../tests/volumes:/opt/src3:ro -p
  gitlabci-local -v ../../tests/local:/opt/src:ro -v ../../tests/volumes:/opt/src:ro -p && exit 1 || true
  gitlabci-local -w /opt/src -p
  gitlabci-local -w /opt/unknown -p || (type podman >/dev/null 2>&1 && echo 'Podman engine: CLI workdir is not created automatically as expected')
fi
gitlabci-local -w . -p
gitlabci-local -r -w . -p
gitlabci-local -w ../../tests/volumes/ -p || (type podman >/dev/null 2>&1 && echo 'Podman engine: CLI workdir is not created automatically as expected')
gitlabci-local -r -w ../../tests/volumes/ -p
gitlabci-local -w . -p
gitlabci-local -r -w . -p
gitlabci-local 'Job 2'
gitlabci-local -w . 'Job 2'
gitlabci-local -r 'Job 2'
gitlabci-local -r -w . 'Job 2'
if [ "${OSTYPE}" = 'msys' ] || [ "${OSTYPE}" = 'win32' ]; then
  gitlabci-local -c ./.gitlab-ci.windows.yml -p || true
else
  gitlabci-local -c ./.gitlab-ci.relative.yml -p
  gitlabci-local -c ./.gitlab-ci.variables.yml -p
fi
gitlabci-local -c ./.gitlab-ci.empty.yml -p && exit 1 || true

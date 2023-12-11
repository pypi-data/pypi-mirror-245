#!/bin/sh

# Access folder
script_path=$(readlink -f "${0}")
test_path=$(readlink -f "${script_path%/*}")
cd "${test_path}/"

# Prepare aliases
alias pexpect-executor='pexpect-executor --delay-init 0.2 --delay-press 0.2 --delay-prompt 0.2'

# Configure tests
set -ex

# Run tests
pexpect-executor --space --enter gitlabci-local
pexpect-executor --press a --enter gitlabci-local
pexpect-executor --press a --enter -- gitlabci-local -s 'Job 1'
pexpect-executor --down --down --space --enter -- gitlabci-local -m
pexpect-executor --space --enter -- gitlabci-local -p -s
pexpect-executor --space --enter -- gitlabci-local -p -s menus-1
pexpect-executor -- gitlabci-local -p -s menus-0
pexpect-executor --up --up --space --enter -- gitlabci-local -p -m -l
pexpect-executor --ctrl c -- gitlabci-local -p -m -l
pexpect-executor --space --enter -- gitlabci-local -c ./.gitlab-ci.select.yml -s
FORCE_COLOR=1 pexpect-executor --enter -- gitlabci-local -c ./.gitlab-ci.select.yml -l
FORCE_COLOR=0 pexpect-executor --enter -- gitlabci-local -c ./.gitlab-ci.select.yml -l

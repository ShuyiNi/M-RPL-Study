#!/usr/bin/env bash
# Set up common environment variables.
#
# Usage:
#   $ source scripts/setup-env.sh
#
set -e

cd "$(dirname "$0")"
cd ..
pwd
export PROJECT_ROOT="$PWD"
export CONTIKI="$PROJECT_ROOT/contiki-ng"
export CONTIKI_DOCKER_IMAGE="contiker/contiki-ng"

set +e

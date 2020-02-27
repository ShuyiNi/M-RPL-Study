#!/usr/bin/env bash

PROJECT_ROOT="$( cd "$( dirname "$0" )"/.. && pwd )"
export PROJECT_ROOT
echo "PROJECT_ROOT=$PROJECT_ROOT"

export CONTIKI_DOCKER_IMAGE="contiki-ng"
echo "CONTIKI_DOCKER_IMAGE=$CONTIKI_DOCKER_IMAGE"

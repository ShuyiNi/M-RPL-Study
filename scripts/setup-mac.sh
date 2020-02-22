#!/usr/bin/env bash
# Usage:
# $ source script/setup-mac.sh
set -e

# Make sure running in project root dir
cd "$(dirname "$0")"
cd ..
pwd

# https://github.com/contiki-ng/contiki-ng/wiki/Docker#with-xquartz
open -a XQuartz
export CNG_PATH="$PWD/contiki-ng"
contiker () {
    COMMAND_STRING="
        cp \${HOME}/dot.Xauthority \${HOME}/.Xauthority
        DISPLAY_NAME=host.docker.internal:0
        export DISPLAY=\${DISPLAY_NAME}.0
        XAUTH_HEXKEY=`xauth list | head -n 1 | awk '{print $3}'`
        xauth add \${DISPLAY_NAME} . \${XAUTH_HEXKEY}
        $@"
    docker run --privileged  \
               --sysctl net.ipv6.conf.all.disable_ipv6=0  \
               --mount type=bind,source="$CNG_PATH",destination=/home/user/contiki-ng  \
               -v ~/.Xauthority:/home/user/dot.Xauthority:ro  \
               -ti contiker/contiki-ng  \
               bash -c "${COMMAND_STRING}"
}

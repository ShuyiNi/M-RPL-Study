#!/usr/bin/env bash

# https://github.com/contiki-ng/contiki-ng/wiki/Docker#with-xquartz
# https://github.com/contiki-ng/contiki-ng/issues/798
open -a XQuartz
contiker () {
    COMMAND_STRING="
        cp \${HOME}/dot.Xauthority \${HOME}/.Xauthority
        DISPLAY_NAME=host.docker.internal:0
        export DISPLAY=\${DISPLAY_NAME}.0
        XAUTH_HEXKEY=$(xauth list | grep /unix | awk '{print $3}')
        xauth add \${DISPLAY_NAME} . \${XAUTH_HEXKEY}
        $*"
    docker run \
        --privileged \
        --sysctl net.ipv6.conf.all.disable_ipv6=0 \
        --mount type=bind,source="$PROJECT_ROOT",destination=/home/user/work \
        -v ~/.Xauthority:/home/user/dot.Xauthority:ro \
        -ti "$CONTIKI_DOCKER_IMAGE" \
        bash -c "${COMMAND_STRING}"
}
command -v contiker

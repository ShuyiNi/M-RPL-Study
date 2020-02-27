#!/usr/bin/env bash

# https://github.com/contiki-ng/contiki-ng/wiki/Docker#setup
contiker () {
    docker run \
        --priviledged \
        --sysctl net.ipv6.conf.all.disable_ipv6=0 \
        --mount type=bind,source="$PROJECT_ROOT",destination=/home/user/work \
        -e DISPLAY="$DISPLAY" \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v /dev/bus/usb:/dev/bus/usb \
        -ti "$CONTIKI_DOCKER_IMAGE" \
        bash -c "$*"
}
command -v contiker

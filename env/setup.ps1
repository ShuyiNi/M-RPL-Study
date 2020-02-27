$PROJECT_ROOT = pwd
$CONTIKI_DOCKER_IMAGE = "contiki-ng"
function contiker {
        docker run --privileged --sysctl net.ipv6.conf.all.disable_ipv6=0 --mount type=bind,source="$PROJECT_ROOT",destination=/home/user/work -e DISPLAY="host.docker.internal:0.0" -ti "$CONTIKI_DOCKER_IMAGE" bash -c "$args"
}
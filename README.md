# CSE-222A-Project
Research project for CSE 222A on RPL-based IoT protocol congestion

## Requirements

- Docker
- git
- XQuartz

## Workflow

Clone the repository:
```console
$ git clone https://github.com/ShuyiNi/CSE-222A-Project.git  # or git@github.com:ShuyiNi/CSE-22
$ cd CSE-222A-Project
$ git submodule update --init --recursive
```

Set up the environment:
```console
$ source script/setup-env.sh
$ source script/setup-mac.sh  # macOS specific
```

Start Cooja:
```
$ contiker cooja
```

```
$CONTIKI/tests/simexec.sh cooja-sim/test/sim.csc "$CONTIKI" cooja-sim/test/sim 1 1
```
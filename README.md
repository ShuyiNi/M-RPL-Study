# RPL Congestion Control
This is a [course](http://cseweb.ucsd.edu/~gmporter/classes/wi20/cse222a/) project.

## Requirements

- git
- Docker
- XQuartz [macOS]

## Workflow

Clone the repository:
```console
$ git clone <repo-url>
$ cd <repo-dir>
$ git submodule update --init --recursive
```

Set up the environment:
```console
$ source env/setup.sh
$ source env/setup-linux.sh  # for Linux
$ source env/setup-macos.sh  # for macOS
```

Build a Docker image from local Dockerfile:
```console
$ make build
```

After above steps, you shall have a Docker image built, and a convenient command `contiker` defined to run the Docker image. This command can be invoked to run various other commands within the Docker container.

To start Cooja:
```
$ contiker cooja
```

To run a Cooja simulation:
```
$ contiker cooja-run cooja-sim/sim.csc  # or
$ contiker make run
```

To auto-format source code
```
$ contiker make fmt
```

Or simple enter the Docker container:
```
$ contiker bash
```

To clean up:
```
$ make clean
$ make distclean
```

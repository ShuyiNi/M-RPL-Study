#!/usr/bin/env bash

SIM_MULTIPAH=0 SIM_N_SRC=5 SIM_PKT_INT=10 cooja-run -t rpl-5-10 sim.csc
SIM_MULTIPAH=1 SIM_N_SRC=5 SIM_PKT_INT=10 cooja-run -t mrpl-5-10 sim.csc

SIM_MULTIPAH=0 SIM_N_SRC=14 SIM_PKT_INT=5 cooja-run -t rpl-14-5 sim.csc
SIM_MULTIPAH=1 SIM_N_SRC=14 SIM_PKT_INT=5 cooja-run -t mrpl-14-5 sim.csc

#!/usr/bin/env bash

cp Makefile.template Makefile
sed -i 's/{{multipath}}/0/g' Makefile
sed -i 's/{{n_src}}/14/g' Makefile
sed -i 's/{{pkt_int}}/5/g' Makefile
make distclean
cooja-run -t rpl-14-5 sim.csc

cp Makefile.template Makefile
sed -i 's/{{multipath}}/1/g' Makefile
sed -i 's/{{n_src}}/14/g' Makefile
sed -i 's/{{pkt_int}}/5/g' Makefile
make distclean
cooja-run -t mrpl-14-5 sim.csc

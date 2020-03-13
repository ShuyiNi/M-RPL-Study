CONTIKI_DOCKER_IMAGE ?= contiki-ng

docker-build:
	docker build . -t $(CONTIKI_DOCKER_IMAGE)

# Commands to run with contiker

compile-m-rpl:
	cd cooja-sim/m-rpl && make node.native

compile-rpl:
	cd cooja-sim/rpl && make node.native

run-m-rpl:
	./bin/cooja-run cooja-sim/m-rpl/sim.csc

run-rpl:
	./bin/cooja-run cooja-sim/rpl/sim.csc

fmt:
	find cooja-sim -name '*.h' -or -name '*.c' -exec clang-format -style=file -i {} \;
	black bin/cooja bin/cooja-run

# Commands runnable without contiker

clean:
	cd cooja-sim && $(MAKE) clean
	rm -rf cooja-sim/log-*

distclean:
	$(MAKE) clean
	cd cooja-sim && $(MAKE) distclean

.PHONY: docker-build compile-m-rpl compile-rpl run-m-rpl run-rpl clean distclean fmt

build:
	docker build . -t $(CONTIKI_DOCKER_IMAGE)

# Commands to run with contiker

compile-test:
	cd cooja-sim/m-rpl && make node.native

run:
	./bin/cooja-run cooja-sim/sim.csc

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

.PHONY: build compile-test run clean distclean fmt

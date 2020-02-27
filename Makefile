build:
	docker build . -t $(CONTIKI_DOCKER_IMAGE)

# Commands to run with contiker

run:
	./bin/cooja-run cooja-sim/sim.csc

fmt:
	find cooja-sim -name '*.h' -or -name '*.c' -exec clang-format -style=file -i {} \;
	black bin/cooja-run

# Commands runnable without contiker

clean:
	cd cooja-sim && $(MAKE) clean
	rm -rf cooja-sim/log-*

distclean:
	$(MAKE) clean
	cd cooja-sim && $(MAKE) distclean

.PHONY: build run clean distclean fmt

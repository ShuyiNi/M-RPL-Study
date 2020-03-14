CONTIKI_DOCKER_IMAGE ?= contiki-ng

docker-build:
	docker build . -t $(CONTIKI_DOCKER_IMAGE)

# Commands to run with contiker

run-test:
	cd experiment/test && ./run-all.sh

fmt:
	# find experiment -name '*.h' -or -name '*.c' -exec clang-format -style=file -i {} \;
	black bin/cooja bin/cooja-process bin/cooja-run

# Commands runnable without contiker

clean:
	cd cooja-sim && $(MAKE) clean
	rm -rf cooja-sim/log-*

distclean:
	$(MAKE) clean
	cd cooja-sim && $(MAKE) distclean

.PHONY: docker-build compile-m-rpl compile-rpl run-m-rpl run-rpl clean distclean fmt

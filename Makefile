CONTIKI_DOCKER_IMAGE ?= contiki-ng

docker-build:
	docker build . -t $(CONTIKI_DOCKER_IMAGE)

# Commands to run with contiker

run-test:
	cd experiment/test && ./run-all.sh

run-all:
	@echo "Starting experiment lodhi15"
	cd experiment/lodhi15 && ./run-all.sh
	@echo "Starting experiment tang15"
	cd experiment/tang15 && ./run-all.sh
	@echo "All experiments finished!"

fmt:
	find experiment -name '*.h' -or -name '*.c' -exec clang-format -style=file -i {} \;
	black experiment
	black bin/cooja bin/cooja-process bin/cooja-run

.PHONY: docker-build run-test run-all fmt

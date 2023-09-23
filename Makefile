build:
	docker build -f docker/Dockerfile -t shield:main .

download_input_data:
	./download_input_data.sh

test:
	docker/docker_run.sh \
		-v $(shell pwd)/input_data:/input_data \
		-v $(shell pwd)/tests:/tests \
		shield:main pytest -vv /tests/test_regression.py

test_regtest_reset:
	docker/docker_run.sh \
		-v $(shell pwd)/input_data:/input_data \
		-v $(shell pwd)/tests:/tests \
		shield:main pytest -vv /tests/test_regression.py --regtest-reset

enter:
	docker/docker_run.sh \
		-v $(shell pwd)/tests:/tests \
		-it shield:main bash

lock_pip:
	pip-compile requirements.in

update_submodules:
	git submodule update --init --recursive
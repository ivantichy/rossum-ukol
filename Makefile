SHELL:=/bin/bash

LAMBDAS = rossum-ukol

STAGE ?= dev
AWS_DEFAULT_REGION ?= eu-central-1

.PHONY: install
install:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv sync --dev

.PHONY: lock
lock:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv lock

.PHONY: lint
lint:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run pylint cdk/
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run mypy cdk/index.py --namespace-packages
	find -name *.py | xargs pipenv run black --line-length 140 --target-version py311 -S --check

.PHONY: test
test:
	for LAMBDA in ${LAMBDAS}; do \
		PIPENV_IGNORE_VIRTUALENVS=1 pipenv run pytest $${LAMBDA}/; \
	done

.PHONY: clean
clean:
	rm -rf cdk.out || /bin/true
	for LAMBDA in ${LAMBDAS}; do \
		make -C $${LAMBDA} clean; \
	done

.PHONY: synth
synth: bundle-lambdas ## synths aws cdk stack
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run \
		env \
		cdk synth > template.yml

.PHONY: deploy
deploy: bundle-lambdas ## deploys aws cdk stack
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run \
		env \
		cdk deploy --require-approval=never

.PHONY: bundle-lambdas
bundle-lambdas: ## Bundles all required lambdas
	@set -e
	for LAMBDA in ${LAMBDAS}; do \
		test -d $${LAMBDA}/build/distributions || make -C $${LAMBDA} bundle; \
	done

.PHONY: rebundle-lambdas
rebundle-lambdas: ## Rebundles all required lambdas
	@set -e
	for LAMBDA in ${LAMBDAS}; do \
		rm -r $${LAMBDA}/build/distributions; \
		make -C $${LAMBDA} bundle; \
	done

.PHONY: format
format:
	find -name *.py | xargs pipenv run black --line-length 140 --target-version py312 -S

.PHONY: run-local
run-local:
	# set up env vars first
	pipenv run fastapi run rossum-ukol/src/lambda_function.py --reload

.PHONY: docker-build
docker-build:
	docker build -t rossum-ukol .

.PHONY: docker-test
docker-test:
	docker run -it rossum-ukol make test

.PHONY: docker-run 
docker-run:
	docker run -it -p 8000:8000 rossum-ukol make run-local

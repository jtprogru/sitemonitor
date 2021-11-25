# Makefile

SHELL := /bin/bash

.PHONY: default test-full isort clean-pyc clean-full


default: test-full

run-f:
	docker compose up --build

run-b:
	docker compose up -d --build

build-img:
	docker build . --tag ghcr.io/jtprogru/sitemonitor:lates

install-deps-prod: requirements.txt
	./venv/bin/pip install -r requirements.txt

pytest: clean-pyc
	./venv/bin/python -m py.test

isort:
	./venv/bin/python -m isort monitoringdaemon/

black:
	./venv/bin/python -m black monitoringdaemon/

flake8:
	./venv/bin/python -m flake8 monitoringdaemon/

test-full: isort black flake8 pytest

clean-full:
	find ./monitoringdaemon -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +

clean-pyc:
	find ./monitoringdaemon -name '*.pyc' -exec rm -f {} +
	find ./monitoringdaemon -name '*.pyo' -exec rm -f {} +

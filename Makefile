PYTHON := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)

.PHONY: test run

test:
	$(PYTHON) -m pytest

run:
	$(PYTHON) -m examples.run_demo

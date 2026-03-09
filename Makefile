.PHONY: init lint test run

PYTHON ?= python3

init:
	$(PYTHON) -m pip install -r requirements.txt

lint:
	$(PYTHON) -m py_compile snapshot/*.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

run:
	$(PYTHON) -m snapshot.service

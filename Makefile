.PHONY: init lint test run

init:
	python -m pip install -r requirements.txt

lint:
	python -m py_compile snapshot/*.py

test:
	python -m unittest discover -s tests -p 'test_*.py'

run:
	python -m snapshot.service

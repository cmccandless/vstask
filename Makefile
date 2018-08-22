all: clean lint test build test

clean:
	- rm -rf build/ dist/ *.egg-info/

init:
	- python -m pip install -r requirements.txt
	
lint:
	- python -m flake8

test:
	- python -m coverage run -m pytest -v

report: lint test
	@echo "coverage report"
	@python -m coverage report || (echo "FAIL: Test coverage threshold is too low" && exit 2)

build:
	- python setup.py sdist bdist_wheel

upload-test:
	- twine upload -r testpypi dist/*

upload:
	- twine upload -r pypi dist/*

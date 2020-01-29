.PHONY: docs

init:
	pip install poetry
	poetry install

reinit:
	poetry env remove python
	make init

test:
	poetry run pytest

publish:
	poetry publish --build

publish-test:
	poetry publish --build -r https://test.pypi.org/

docs:
	cd docs && poetry run make html

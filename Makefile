.PHONY: docs

init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	pipenv run pytest

flake8:
	pipenv run flake8 --ignore=E501,F401,E128,E402,E731,F821 tabler

publish:
	pipenv run pip install 'twine>=1.5.0'
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf build dist .egg tabler.egg-info

publish-test:
	pipenv run pip install 'twine>=1.5.0'
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	rm -rf build dist .egg tabler.egg-info

docs:
	cd docs && pipenv run make html

lock:
	pipenv lock -dr > requirements.txt
docs:
	sphinx-build docs/ docs/_build/

site: docs
	rsync -avkz site/ tarf:sites/psa/

build:
	python setup.py sdist
	python setup.py bdist_wheel --python-tag py2
	BUILD_VERSION=3 python setup.py bdist_wheel --python-tag py3

publish: build
	python setup.py upload

clean:
	find . -name '*.py[co]' -delete
	find . -name '__pycache__' -delete
	rm -rf python_social_auth.egg-info dist build

.PHONY: site docs publish

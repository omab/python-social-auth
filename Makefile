docs:
	sphinx-build docs/ docs/_build/

site: docs
	rsync -avkz site/ tarf:sites/psa/

build:
	python setup.py sdist
	python setup.py bdist_wheel --python-tag py2
	BUILD_VERSION=3 python setup.py bdist_wheel --python-tag py3

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel --python-tag py2 upload
	BUILD_VERSION=3 python setup.py bdist_wheel --python-tag py3 upload

run-tox:
	@ tox

docker-tox-build:
	@ docker build -t omab/psa-legacy .

docker-tox: docker-tox-build
	@ docker run -it --rm \
		     --name psa-legacy-test \
		     -v "`pwd`:/code" \
		     -w /code omab/psa-legacy tox

docker-shell: docker-tox-build
	@ docker run -it --rm \
		     --name psa-legacy-test \
		     -v "`pwd`:/code" \
		     -w /code omab/psa-legacy bash

clean:
	@ find . -name '*.py[co]' -delete
	@ find . -name '__pycache__' -delete
	@ rm -rf *.egg-info dist build


.PHONY: site docs publish

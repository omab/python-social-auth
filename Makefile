build:
	python setup.py sdist
	python setup.py bdist_wheel --python-tag py2
	BUILD_VERSION=3 python setup.py bdist_wheel --python-tag py3

publish:
	python setup.py sdist upload
	python setup.py bdist_wheel --python-tag py2 upload
	BUILD_VERSION=3 python setup.py bdist_wheel --python-tag py3 upload

docker-tox-build:
	@ docker build -t omab/psa-legacy .

docker-tox: docker-tox-build
	@ docker run -it --rm \
		     --name psa-legacy-test \
		     -v "`pwd`:/code" \
		     -w /code omab/psa-legacy tox

clean:
	@ find . -name '*.py[co]' -delete
	@ find . -name '__pycache__' -delete
	@ rm -rf *.egg-info dist build

docs:
	sphinx-build docs/ docs/_build/

site: docs
	rsync -avkz site/ tarf:sites/psa/

publish:
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: site docs publish

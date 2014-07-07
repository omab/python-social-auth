docs:
	sphinx-build docs/ docs/_build/

site: docs
	rsync -avkz site/ tarf:sites/psa/

.PHONY: site docs

#!/bin/bash

# 1. Install pyenv
# 2. Install python versions
#      pyenv install 2.7.11
#      pyenv install 3.3.6
#      pyenv install 3.4.4
#      pyenv install pypy-4.0.1
# 3. Switch to each version and install / update setuptools, pip, tox
#      pip install -U setuptools pip tox
# 4. Enable versions
#      pyenv local 2.7.11 3.3.6 3.4.4 pypy-4.0.1
# 5. Run tox

which pyenv && eval "$(pyenv init -)"
tox

#!/bin/bash

which pyenv && eval "$(pyenv init -)"
tox

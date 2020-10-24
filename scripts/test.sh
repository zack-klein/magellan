set -ex

black magellan --line-length 79 --check

flake8 magellan

coverage run -m pytest -v && coverage report -m

set -ex

black magellan --line-length 79

flake8 magellan

pytest -v

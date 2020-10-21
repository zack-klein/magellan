set -ex

black magellan --line-length 79 --check

flake8 magellan

pytest -v tests

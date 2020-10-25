set -ex

pip check

black magellan --line-length 79 --check

flake8 magellan

bandit -r -lll magellan

coverage run -m pytest -v && coverage report -m

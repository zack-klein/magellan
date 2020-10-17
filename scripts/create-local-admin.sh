set -ex

export FLASK_APP=magellan

flask fab create-admin --username admin --password admin --firstname admin --lastname admin --email admin

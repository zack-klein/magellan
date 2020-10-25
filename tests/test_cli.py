from unittest.mock import patch

from magellan.cli import Magellan


@patch("magellan.cli.app")
def test_webserver_calls_app_run(app_mock):
    Magellan().webserver(None)
    app_mock.run.assert_called_once()


@patch("magellan.cli.upgrade")
def test_upgradedb_calls_flask_migrate(upgrade_mock):
    Magellan().upgradedb()
    upgrade_mock.assert_called_once()


@patch("magellan.cli.downgrade")
def test_downgradedb_calls_flask_migrate(downgrade_mock):
    Magellan().downgradedb()
    downgrade_mock.assert_called_once()

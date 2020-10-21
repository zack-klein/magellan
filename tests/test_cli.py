from unittest.mock import patch

from magellan.cli import Magellan


@patch("magellan.cli.app")
def test_webserver_calls_app_run(app_mock):
    Magellan().webserver(None)
    app_mock.run.assert_called_once()

"""
Tests the presentation logic of the Flask application.
"""

import pytest

from magellan import app  # create_app
from magellan.app.database import db


@pytest.fixture
def client():
    # app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client


def test_home_page(client):
    assert b"Magellan" in client.get("/").data


def test_not_logged_in_cant_see_admin_panes(client):
    assert b"Govern" not in client.get("/").data
    assert b"Analyze" not in client.get("/").data
    assert b"Find Data" not in client.get("/").data


def test_not_logged_in_gets_login_page(client):
    assert b"Username" in client.get("/login/").data

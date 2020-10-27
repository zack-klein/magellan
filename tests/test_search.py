import datetime

from tests.utils import (
    client,
    admin_login,
    get_admin,
    logout,
    build_dummy_data,
    DUMMY_TAG,
)

from magellan.app import models
from magellan.app.database import db


def test_not_logged_in_cant_see_search(client):
    assert client.get("/search/").status_code != 200


def test_admin_can_see_search(client):
    admin_login(client)
    assert client.get("/search/").status_code == 200


def test_tags_suggested_for_search(client):
    admin_login(client)
    build_dummy_data(client)
    assert bytes(DUMMY_TAG, "utf-8") in client.get("/search/").data

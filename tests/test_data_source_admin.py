from tests.test_app import client, admin_login, get_admin, logout  # noqa
from tests.test_search import build_dummy_data, DUMMY_DATA_SOURCE

from magellan.app import models
from magellan.app.database import db


def test_not_logged_in_cannot_see_admin(client):  # noqa
    """
    Tests that not logged in user can't see the data source admin view.
    """
    assert client.get("/sources/list/").status_code != 200


def test_admin_gets_200(client):  # noqa
    """
    Tests that a logged in user can see the data source admin view.
    """
    admin_login(client)
    assert client.get("/sources/list/").status_code == 200


def test_connection_string_not_in_show_view(client):  # noqa
    """
    Tests that connection strings don't show up in the data source show view.
    """
    build_dummy_data(client)
    admin_login(client)
    ds = (
        db.session.query(models.DataSource)
        .filter(models.DataSource.name == DUMMY_DATA_SOURCE)
        .first()
    )
    assert client.get(f"/sources/show/{ds.id}").status_code == 200
    assert (
        bytes(ds.connection_string, "utf-8")
        not in client.get(f"/sources/show/{ds.id}").data
    )


def test_connection_string_not_in_edit_view(client):  # noqa
    """
    Tests that connection strings don't show up in the data source edit view.
    """
    build_dummy_data(client)
    admin_login(client)
    ds = (
        db.session.query(models.DataSource)
        .filter(models.DataSource.name == DUMMY_DATA_SOURCE)
        .first()
    )
    assert client.get(f"/sources/edit/{ds.id}").status_code == 200
    assert (
        bytes(ds.connection_string, "utf-8")
        not in client.get(f"/sources/edit/{ds.id}").data
    )


def test_connection_string_not_in_list_view(client):  # noqa
    """
    Tests that connection strings don't show up in the data source list view.
    """
    build_dummy_data(client)
    admin_login(client)
    ds = (
        db.session.query(models.DataSource)
        .filter(models.DataSource.name == DUMMY_DATA_SOURCE)
        .first()
    )
    assert client.get(f"/sources/list/").status_code == 200
    assert (
        bytes(ds.connection_string, "utf-8")
        not in client.get(f"/sources/list/").data
    )

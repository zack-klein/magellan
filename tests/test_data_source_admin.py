from tests.test_app import client, admin_login, get_admin, logout  # noqa


def test_not_logged_in_cannot_see_admin(client):  # noqa
    assert client.get("/sources/list/").status_code != 200


def test_admin_gets_200(client):  # noqa
    admin_login(client)
    assert client.get("/sources/list/").status_code == 200

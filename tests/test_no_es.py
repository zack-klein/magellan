from tests.test_app import client, admin_login, get_admin, logout  # noqa


def test_no_es_warning_does_not_show_for_anonymous(client):  # noqa
    assert b"No elasticsearch running!" not in client.get("/").data


def test_no_es_warning_shows_for_admins(client):  # noqa
    admin_login(client)
    assert b"No elasticsearch running!" in client.get("/").data
    assert b"No elasticsearch running!" in client.get("/search/").data
    logout(client)

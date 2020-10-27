from tests.utils import admin_login, logout, client


def test_home_page(client):
    assert b"Magellan" in client.get("/").data


def test_not_logged_in_cant_see_admin_panes(client):
    assert b"Govern" not in client.get("/").data
    assert b"Analyze" not in client.get("/").data
    assert b"Find Data" not in client.get("/").data


def test_not_logged_in_gets_login_page(client):
    assert b"Username" in client.get("/login/").data
    assert b"Password" in client.get("/login/").data
    assert b"Sign In" in client.get("/login/").data


def test_logged_in_admin_sees_all_index_bars(client):
    admin_login(client)
    assert b"Security" in client.get("/").data
    assert b"Find Data" in client.get("/").data
    assert b"Govern" in client.get("/").data
    assert b"Analyze" in client.get("/").data
    logout(client)

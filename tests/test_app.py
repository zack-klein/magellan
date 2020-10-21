"""
Tests the presentation logic of the Flask application.
"""

import pytest

from magellan import app
from magellan.app.database import db


# from flask_appbuilder.security.sqla.models import Role


FAKE_ADMIN_USER = "Indiana Jones"
FAKE_ADMIN_FN = "Indiana"
FAKE_ADMIN_LAST = "Jones"
FAKE_ADMIN_EMAIL = "indiana@jones.com"
FAKE_ADMIN_PASS = "I'm too old for this ish."


def create_dummy_user(client):
    pass
    # role_admin = current_app.appbuilder.sm.find_role(
    #     current_app.appbuilder.sm.auth_role_admin
    # )
    # # if not role_admin:
    # roles = db.session.query(Role).all()
    # print(f"ROLES ARE: {roles}")
    # print(f"ROLE ADMIN IS: {role_admin}")
    # user = current_app.appbuilder.sm.add_user(
    #     FAKE_ADMIN_USER,
    #     FAKE_ADMIN_FN,
    #     FAKE_ADMIN_LAST,
    #     FAKE_ADMIN_EMAIL,
    #     role_admin,
    #     FAKE_ADMIN_PASS,
    # )


def login(client, username, password):
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            from magellan.app import views, models  # noqa

            yield client
            db.drop_all()


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


# TODO: I can't for the life of me get login functionality to work in the
# tests. My suspicion is it is because of some flask_appbuilder internals,
# but it should get figured out.

"""
Tests the presentation logic of the Flask application.
"""
import logging

import pytest

from flask import current_app

from flask_appbuilder.security.sqla.models import (
    User,
    PermissionView,
)

from magellan import app
from magellan.app.database import db

from flask_appbuilder.security.sqla.models import Role


FAKE_ADMIN_USER = "Indiana Jones"
FAKE_ADMIN_FN = "Indiana"
FAKE_ADMIN_LAST = "Jones"
FAKE_ADMIN_EMAIL = "indiana@jones.com"
FAKE_ADMIN_PASS = "I'm too old for this ish."


# TODO: Move all this set up stuff into a tests/utils.py
def create_admin_role():
    current_app.appbuilder.add_permissions(update_perms=False)
    role_name = app.config["AUTH_ROLE_ADMIN"]
    permission_views = db.session.query(PermissionView).all()
    logging.warning(
        f"Admin role doesn't exist. Creating: '{role_name}' "
        f"with permissions: {permission_views}"
    )

    role = Role(
        name=role_name,
        permissions=permission_views,
    )
    db.session.add(role)
    db.session.commit()


def create_dummy_user(client):
    role_admin = (
        db.session.query(Role)
        .filter(Role.name == app.config["AUTH_ROLE_ADMIN"])
        .first()
    )
    current_app.appbuilder.sm.add_user(
        FAKE_ADMIN_USER,
        FAKE_ADMIN_FN,
        FAKE_ADMIN_LAST,
        FAKE_ADMIN_EMAIL,
        role_admin,
        FAKE_ADMIN_PASS,
    )


def admin_login(client):
    return client.post(
        "/login",
        data=dict(username=FAKE_ADMIN_USER, password=FAKE_ADMIN_PASS),
        follow_redirects=True,
    )


def get_admin():
    return (
        db.session.query(User).filter(User.username == FAKE_ADMIN_USER).first()
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["CSRF_ENABLED"] = False
    app.config["WTF_CSRF_ENABLED"] = False
    app.elasticsearch = None

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            from magellan.app import views, models  # noqa

            logging.warning(f"DB Connection: {db.engine}")
            create_admin_role()
            create_dummy_user(client)

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


def test_logged_in_admin_sees_all_index_bars(client):
    admin_login(client)
    assert b"Security" in client.get("/").data
    assert b"Find Data" in client.get("/").data
    assert b"Govern" in client.get("/").data
    assert b"Analyze" in client.get("/").data

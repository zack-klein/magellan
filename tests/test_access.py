from flask_appbuilder.security.sqla.models import Role

from tests.utils import (
    client,
    admin_login,
    get_admin,
    logout,
    build_dummy_data,
    DUMMY_TAG,
    DUMMY_DATA_SOURCE,
    DUMMY_DATASET,
)

from magellan import app
from magellan.app import models
from magellan.app.database import db


def test_browse_gets_access_denied(client):
    admin_login(client)
    build_dummy_data(client)
    dataset = (
        db.session.query(models.Dataset)
        .filter(models.Dataset.name == DUMMY_DATASET)
        .first()
    )
    assert client.get(f"/search/browse/{dataset.id}").status_code == 403


def test_browse_shows_results(client):
    admin_login(client)
    build_dummy_data(client)
    ds = (
        db.session.query(models.DataSource)
        .filter(models.DataSource.name == DUMMY_DATA_SOURCE)
        .first()
    )
    role_admin = (
        db.session.query(Role)
        .filter(Role.name == app.config["AUTH_ROLE_ADMIN"])
        .first()
    )
    ds.roles = [role_admin]
    db.session.add(ds)
    db.session.commit()
    dataset = (
        db.session.query(models.Dataset)
        .filter(models.Dataset.name == DUMMY_DATASET)
        .first()
    )
    assert (
        bytes(DUMMY_TAG, "utf-8")
        in client.get(f"/search/browse/{dataset.id}").data
    )


def test_query_gets_access_denied(client):
    admin_login(client)
    build_dummy_data(client)
    dataset = (
        db.session.query(models.Dataset)
        .filter(models.Dataset.name == DUMMY_DATASET)
        .first()
    )
    assert client.get(f"console/?dataset={dataset.id}").status_code != 200
    assert (
        bytes(dataset.name, "utf-8")
        not in client.get(f"console/?dataset={dataset.id}").data
    )


def test_query_has_access(client):
    admin_login(client)
    build_dummy_data(client)
    ds = (
        db.session.query(models.DataSource)
        .filter(models.DataSource.name == DUMMY_DATA_SOURCE)
        .first()
    )
    role_admin = (
        db.session.query(Role)
        .filter(Role.name == app.config["AUTH_ROLE_ADMIN"])
        .first()
    )
    ds.roles = [role_admin]
    db.session.add(ds)
    db.session.commit()
    dataset = (
        db.session.query(models.Dataset)
        .filter(models.Dataset.name == DUMMY_DATASET)
        .first()
    )
    assert client.get(f"console/?dataset={dataset.id}").status_code == 200
    assert (
        bytes(dataset.name, "utf-8")
        in client.get(f"console/?dataset={dataset.id}").data
    )

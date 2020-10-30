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


def test_browse_shows_go_to_admin(client):
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
        bytes("Edit Dataset", "utf-8")
        in client.get(f"/search/browse/{dataset.id}").data
    )

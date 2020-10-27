import logging
import datetime

import pytest

from flask import current_app

from flask_appbuilder.security.sqla.models import (
    User,
    # PermissionView,
)

from magellan import app
from magellan.app import models
from magellan.app.database import db

from flask_appbuilder.security.sqla.models import Role


FAKE_ADMIN_USER = "Indiana Jones"
FAKE_ADMIN_FN = "Indiana"
FAKE_ADMIN_LAST = "Jones"
FAKE_ADMIN_EMAIL = "indiana@jones.com"
FAKE_ADMIN_PASS = "I'm too old for this ish."


def create_dummy_admin(client):
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


DUMMY_DATA_SOURCE = "Top secret information"
DUMMY_DESCRIPTION = "It's really top secret!"
DUMMY_CONNECTION_STRING = "s3://foo/bar"
DUMMY_DATA_SOURCE_TYPE = models.DataSourceTypes.s3_bucket
DUMMY_TAG = "Top Secret"
DUMMY_DATASET = "Something top secret"
DUMMY_DATASET_TYPE = models.DataItemTypes.csv
DUMMY_SCHEMA = "foobarbaz"
DUMMY_COMMENT = "Et tu, Brute?"


def build_dummy_data(client):  # noqa
    user = get_admin()
    data_source = models.DataSource(
        name=DUMMY_DATA_SOURCE,
        description=DUMMY_DESCRIPTION,
        connection_string=DUMMY_CONNECTION_STRING,
        type=DUMMY_DATA_SOURCE_TYPE,
    )
    tag = models.DatasetTag(name=DUMMY_TAG)
    dataset = models.Dataset(
        name=DUMMY_DATASET,
        schema=DUMMY_SCHEMA,
        description=DUMMY_DESCRIPTION,
        type=DUMMY_DATASET_TYPE,
    )
    dataset.data_source = data_source
    dataset.tags = [tag]
    db.session.add_all(
        [
            dataset,
            data_source,
            tag,
        ]
    )

    db.session.commit()

    # Comment needs a valid dataset ID
    comment = models.DatasetComment(
        comment=DUMMY_COMMENT,
        user_id=user.id,
        dataset_id=dataset.id,
        commented_at=datetime.datetime.now(),
    )
    db.session.add(comment)
    db.session.commit()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["CSRF_ENABLED"] = False
    app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            from magellan.app import views, models  # noqa

            logging.warning(f"DB Connection: {db.engine}")
            current_app.appbuilder.sm.create_db()
            current_app.appbuilder.add_permissions(update_perms=True)
            current_app.appbuilder.sm.create_db()
            create_dummy_admin(client)

            yield client
            db.drop_all()

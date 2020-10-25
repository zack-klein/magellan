import datetime

from magellan.app import models
from magellan.app.database import db

from tests.test_app import client, admin_login, get_admin, logout  # noqa


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


def test_dummy_data_exists(client):  # noqa
    admin_login(client)
    build_dummy_data(client)
    logout(client)

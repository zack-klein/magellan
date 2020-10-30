from magellan.app import models
from magellan.app.database import db

from magellan import app
from magellan.extractors import s3, sqlalchemy

from flask_appbuilder.security.sqla.models import Role


EXTRACTORS = {
    models.DataSourceTypes.sqlalchemy: sqlalchemy.extractor,
    models.DataSourceTypes.s3_bucket: s3.extractor,
}


def extract_datasets(data_source, extractors=EXTRACTORS):
    """
    Extracts datasets from any of the supported types and adds them to the
    backend DB.
    """
    extractor = extractors.get(data_source.type)
    datasets = extractor(data_source)

    role_admin = (
        db.session.query(Role)
        .filter(Role.name == app.config["AUTH_ROLE_ADMIN"])
        .first()
    )

    datasets_to_add = []

    for dataset in datasets:

        # Enforce any dataset tags
        for tag in data_source.tags:

            if tag not in dataset.tags:
                dataset.tags.append(tag)

        datasets_to_add.append(dataset)

    data_source.roles += [role_admin]

    db.session.add(data_source)
    db.session.add_all(datasets_to_add)

    db.session.commit()

    return datasets

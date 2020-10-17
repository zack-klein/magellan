from magellan.app import models
from magellan.app.database import db

from magellan.extractors import s3, sqlalchemy


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

    # Make sure each dataset has required tags
    rules = (
        db.session.query(models.DataSourceRule)
        .filter(models.DataSourceRule.data_source_id == data_source.id)
        .all()
    )

    required_tags = []
    for rule in rules:

        if rule.tags:
            required_tags += rule.tags

    for dataset in datasets:

        # Enforce any dataset rules
        for tag in required_tags:

            if tag not in dataset.tags:
                dataset.tags.append(tag)

        db.session.add(dataset)

    db.session.commit()
    return datasets

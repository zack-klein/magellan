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

    for dataset in datasets:

        # Enforce any dataset tags
        for tag in data_source.tags:

            if tag not in dataset.tags:
                dataset.tags.append(tag)

        db.session.add(dataset)

    db.session.commit()
    return datasets

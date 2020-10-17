from sqlalchemy import create_engine, inspect

from magellan.app import models
from magellan.app.database import db


def extractor(data_source):
    """
    Extracts data from a SQLAlchemy connection.
    """
    datasets = []
    engine = create_engine(data_source.connection_string)
    inspector = inspect(engine)

    schemas = inspector.get_schema_names()

    for schema in schemas:

        tables = inspector.get_table_names(schema=schema)

        for table in tables:

            # TODO: Add column-level detail

            existing_table = (
                db.session.query(models.Dataset)
                .filter(models.Dataset.name == table)
                .filter(models.Dataset.data_source_id == data_source.id)
                .first()
            )

            if existing_table:
                dataset = existing_table
            else:
                dataset = models.Dataset(
                    name=table,
                    type=models.DataItemTypes.table,  # TODO: Don't hard code
                    schema=schema,
                    data_source_id=data_source.id,
                )
            datasets.append(dataset)

    return datasets

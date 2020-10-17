import pandas as pd

from sqlalchemy import create_engine


def sampler(dataset, numrows=10):
    """
    Grab some sample data from a SQLAlchemy source.
    """
    query = f"select * from {dataset.schema}.{dataset.name}"
    if numrows:
        query += f" limit {numrows};"
    else:
        query += ";"
    engine = create_engine(dataset.data_source.connection_string)
    df = pd.read_sql(query, engine)
    return df

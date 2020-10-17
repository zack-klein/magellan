import os

import pandas as pd

from urllib.parse import urlparse


READERS = {
    ".csv": pd.read_csv,
    ".json": pd.read_json,
}


def sampler(dataset, numrows=10, readers=READERS):
    """
    Grab a sample of some data in S3.
    """
    url = urlparse(
        dataset.data_source.connection_string, allow_fragments=False
    )
    bucket = url.netloc
    try:
        # TODO: Add logic for inferring file type more intelligently
        s3_key = f"s3://{bucket}/{dataset.name}"
        file_type = os.path.splitext(s3_key)[1]
        reader = readers.get(file_type, pd.read_csv)
        df = reader(s3_key, nrows=numrows)
    except Exception as e:
        df = e
    return df

import json

from urllib.parse import urlparse

import boto3

from magellan.app import models  # , logger
from magellan.app.database import db

import logging

logger = logging.getLogger(__name__)


def get_all_s3_keys(s3_uri, list_objects_v2_kwargs={}):
    """Get a list of all keys in an S3 bucket."""
    s3 = boto3.client("s3", region_name="eu-central-1")
    url = urlparse(s3_uri, allow_fragments=False)
    bucket = url.netloc
    key_prefix = url.path.lstrip("/")

    keys = []
    kwargs = list_objects_v2_kwargs
    kwargs["Bucket"] = bucket
    kwargs["Prefix"] = key_prefix

    callnum = 0
    logger.warning(f"Calling {bucket} with kwargs: {kwargs}...")
    while True:

        callnum += 1

        if callnum % 10 == 0:
            logger.warning(f"Making call {callnum} to {bucket}...")

        resp = s3.list_objects_v2(**kwargs)

        for obj in resp["Contents"]:
            keys.append(obj["Key"])

        try:
            kwargs["ContinuationToken"] = resp["NextContinuationToken"]
        except KeyError:
            break

    logger.info(f"Found len({keys}) keys in {bucket}!")

    return keys


def extractor(data_source):
    """
    Extracts data from an S3 bucket.
    """
    datasets = []

    try:
        client_kwargs = json.loads(data_source.extras)

    except Exception:
        logger.warning("Failed to read extras. Not passing extras...")
        client_kwargs = {}

    keys = get_all_s3_keys(
        data_source.connection_string, list_objects_v2_kwargs=client_kwargs
    )

    for key in keys:
        # TODO: Use https://github.com/ahupp/python-magic to figure out file
        # types so we can extract columns

        existing_dataset = (
            db.session.query(models.Dataset)
            .filter(models.Dataset.name == key)
            .filter(models.Dataset.data_source_id == data_source.id)
            .first()
        )

        if existing_dataset:
            dataset = existing_dataset
        else:
            dataset = models.Dataset(
                name=key,
                type=models.DataItemTypes.table,  # TODO: Add file type
                schema=data_source.connection_string,
                data_source_id=data_source.id,
            )

        datasets.append(dataset)

    return datasets

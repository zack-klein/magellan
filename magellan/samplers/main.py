"""
Gets samples of datasets from all of the supported backends.
"""
import pandas as pd

from magellan.app import models

from magellan.samplers import s3, sqlalchemy


SAMPLERS = {
    models.DataSourceTypes.sqlalchemy: sqlalchemy.sampler,
    models.DataSourceTypes.s3_bucket: s3.sampler,
}


def get_df(dataset, numrows=10, samplers=SAMPLERS):
    """
    Grab a dataframe.
    """
    sampler = samplers.get(dataset.data_source.type)
    df = sampler(dataset, numrows=numrows)

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame()

    return df


def df_to_html(df, msg="An error occurred when trying to load the table"):
    """"""
    if df.empty:
        html = f"""
            <div class="col">
                <i>{msg}</i>
            </div>
            <br>
        """
    else:
        html = df.to_html(index=False, classes=("table"), border=0)
    return html


def mask_field(row):
    return "*" * len(row)


def get_sample_data(dataset, masked_fields=[], numrows=10, samplers=SAMPLERS):
    """
    Grabs a sample from a dataset
    """
    sample_df = get_df(dataset, numrows=numrows)

    for field in masked_fields:

        if field in sample_df.columns:
            sample_df[field] = sample_df[field].apply(mask_field)

    html = df_to_html(sample_df)
    return html

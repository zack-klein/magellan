from pandasql import sqldf

from flask import flash

from magellan.samplers.main import get_df, df_to_html


def clean_table_name(table_name):
    return table_name.replace("/", "").replace(".", "").replace("-", "")


def query_dataset(dataset, query):

    df = get_df(dataset, numrows=None)
    clean_df_name = clean_table_name(dataset.name)
    locals()[clean_df_name] = df
    try:
        returned_df = sqldf(query, locals())
        returned_html = df_to_html(returned_df, msg="Table returned 0 results")
        flash("Query ran successfully!", "success")
    except Exception as e:
        flash("An error occured!", "danger")
        returned_html = f"<code>{str(e)}</code>"
    return returned_html

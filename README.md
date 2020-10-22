# Magellan

A simple but powerful Data Catalog built on top of Flask, Elasticsearch, and pandas.

# Getting started

:warning: **WARNING:** This package is not yet available on PyPi! This getting started guide is not quite accurate -- but it will be soon. Stay tuned.

```
pip install magellan-catalog
```

:warning: **WARNING:** To really leverage Magellan, you should use it with Elasticsearch. You can bring your own Elasticsearch (running locally or via a hosted service like AWS Elasticsearch). Just point Magellan to your Elasticsearch endpoint by setting the following environment variable:

```
MAGELLAN__ELASTICSEARCH_URL=localhost:9200
```

:white_check_mark: That's all you need! Magellan is now ready to go:

```
magellan webserver
```

Head to http://localhost:8080/ to see the web interface. You'll hit the login screen.

![](./docs/imgs/splash.png)

Next, go ahead and create an admin user:

```
magellan create-admin
```


:warning: **WARNING:** You should really only create *the first user* via the CLI. Other users can be handled via the Flask FAB UI.

# Features

## Automatically extract metadata-based `Dataset`s from existing sources

The core concept in Magellan is the `Dataset`

- Create a `Source`
- Specify a connection string (S3 bucket or SQLAlchemy connection string)
- Extract some data!

Supported `Source`s:
- Most databases (anything supported by [SQLAlchemy](https://docs.sqlalchemy.org/))
- [AWS S3](https://aws.amazon.com/s3)
- ... and more to come!

## Tag `Source`s and `Dataset`s with useful metadata en masse

Magellan allows you to create `Rule`s that will apply searchable `Tag`s to Datasets at extraction time. A few clicks and thousands of entries of useful metadata will be created.

## Blazing fast search with Elasticsearch

All objects in Magellan are automatically indexed in Elasticsearch -- allowing you to access them simply and easily from a Google-style search bar.

## Backend-agnostic SQL console

Once you have found data you find interesting in Magellan, a backend-agnostic SQL console lets you query the data interactively to answer all the questions you may have.

## Discuss datasets with other users

Comment feature allows different users to comment and collaborate on datasets.

## Modular backend and core components
Bring your own SQL backend and Elasticsearch to help you scale to whatever size your data catalog needs.

# Roadmap

- Granular security permissions
- Robust CLI
- Cross-dataset, backend-agnostic SQL console
- Integration with [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling)
- ... and more!

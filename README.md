# Magellan

![Magellan Cartoon](./docs/imgs/magellan.png)

A simple but powerful Data Catalog built on top of Flask, Elasticsearch, and pandas.

- [Magellan](#magellan)
- [Getting started](#getting-started)
- [Features](#features)
  * [Automatically extract metadata-based `Dataset`s from existing sources](#automatically-extract-metadata-based--dataset-s-from-existing-sources)
  * [Tag `Source`s and `Dataset`s with useful metadata en masse](#tag--source-s-and--dataset-s-with-useful-metadata-en-masse)
  * [Blazing fast search with Elasticsearch](#blazing-fast-search-with-elasticsearch)
  * [Backend-agnostic SQL console](#backend-agnostic-sql-console)
  * [Discuss datasets with other users](#discuss-datasets-with-other-users)
  * [Modular backend and components](#modular-backend-and-components)
- [Roadmap](#roadmap)

# Getting started

:warning: This package is not yet available on PyPi! This getting started guide is not quite accurate -- but it will be soon. Stay tuned.

```
pip install magellan-catalog
```

:warning: Magellan will only work if you have Elasticsearch running!

Point Magellan to your Elasticsearch instance by setting the environment variable:

```
MAGELLAN__ELASTICSEARCH_URL=localhost:9200
```

Then Magellan is ready to go!

```
magellan webserver
```

Head to http://localhost:8080/ to see the web interface. You'll hit the login screen, so go ahead and create a user:

```
magellan create-user
```

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

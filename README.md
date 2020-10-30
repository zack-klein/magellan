# Magellan

A simple but powerful Data Catalog built on top of [Flask](https://readthedocs.org/projects/flask/), [Elasticsearch](https://www.elastic.co/guide/en/elastic-stack-get-started/current/index.html), and [Pandas](https://pandas.pydata.org/).

:warning: **DISCLAIMER:** This package is still under active development and isn't quite production ready. For this reason, I've chosen to not list it on PyPi (yet!). That said, please use it! Any and all contributions are welcome. Once it has been battle tested it will be listed on PyPi and installation will be typical for a Python package. Stay tuned!

# Getting started

Installation is done via git:

```bash
git clone https://github.com/zack-klein/magellan.git
cd ./magellan
pip install .
```

:memo: **NOTE:** To really leverage Magellan, you should use it with [Elasticsearch](https://www.elastic.co/guide/en/elastic-stack-get-started/current/index.html). You can bring your own Elasticsearch (running locally or via a hosted service like AWS Elasticsearch Service). Just point Magellan to your Elasticsearch endpoint by setting the following environment variable:

```bash
export MAGELLAN__ELASTICSEARCH_URL=localhost:9200
```

Next up, you'll want to initialize the database:
```bash
magellan initdb
```

After the database has been created, you can create the first user:

```bash
magellan create-admin
```

:white_check_mark: That's all you need! Magellan is now ready to go:

```
magellan webserver
```

Head to http://localhost:8080/ to see the web interface. You'll hit the login screen.

![](./docs/imgs/splash.png)

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

Magellan allows you to apply searchable `Tag`s to Datasets at extraction time. A few clicks and thousands of entries of useful metadata will be created.

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

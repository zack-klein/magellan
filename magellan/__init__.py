from flask import Flask

from elasticsearch import Elasticsearch

from magellan.app.database import db
from magellan.app.fab import appbuilder
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object("magellan.config")

Bootstrap(app)
db.init_app(app)

es_url = (
    app.config["ELASTICSEARCH_URL"]
    if app.config["ELASTICSEARCH_URL"]
    else None
)
app.elasticsearch = Elasticsearch(es_url)

with app.app_context():
    appbuilder.init_app(
        app, db.session,
    )
    from magellan.app import views, models  # noqa

from flask import Flask
from flask import flash

from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from flask_login import current_user

from elasticsearch import Elasticsearch

from magellan.app.database import db
from magellan.app.fab import appbuilder


app = Flask(__name__)
app.config.from_object("magellan.config")

Bootstrap(app)
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

es_url = (
    app.config["ELASTICSEARCH_URL"]
    if app.config["ELASTICSEARCH_URL"]
    else None
)
if es_url:
    app.elasticsearch = Elasticsearch(es_url)
else:
    app.elasticsearch = None

with app.app_context():
    appbuilder.init_app(
        app,
        db.session,
    )
    from magellan.app import views, models  # noqa

    @app.before_request
    def before_request():
        if current_user.is_authenticated and not app.elasticsearch:
            flash(
                "No elasticsearch running! Search functionality will be "
                "severely degraded.",
                "danger",
            )

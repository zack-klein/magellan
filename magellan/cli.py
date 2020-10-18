import logging

import fire

# TODO: Use these to dynamically create roles from the CLI based on
# user-provided conditions
from flask_appbuilder.security.sqla.models import User  # noqa
from flask_appbuilder.security.sqla.models import Role  # noqa


logger = logging.getLogger(__name__)


class Magellan:
    def webserver(self, host="0.0.0.0", port=8080, debug=True):
        from magellan import create_app

        app = create_app()
        app.run(host=host, port=port, debug=debug)

    def initdb(self):
        from magellan import create_app
        from magellan.app.database import db

        logger.warning("Creating database objects...")

        app = create_app()

        with app.app_context():
            db.create_all()

        logger.warning("Database created successfully!")


def main():
    fire.Fire(Magellan)

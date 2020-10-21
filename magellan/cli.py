import logging

import fire


from flask import current_app
from flask_appbuilder.security.sqla.models import User  # noqa
from flask_appbuilder.security.sqla.models import Role


logger = logging.getLogger(__name__)


class Magellan:
    def webserver(self, host="0.0.0.0", port=8080, debug=True):
        from magellan import app

        app.run(host=host, port=port, debug=debug)

    def initdb(self):
        from magellan import app
        from magellan.app.database import db

        logger.warning("Creating database objects...")
        with app.app_context():
            db.create_all()

        logger.warning("Database created successfully!")

    def create_admin(self, username, firstname, lastname, email, password):
        from magellan import app
        from magellan.app.database import db

        logger.warning("Creating database objects...")
        with app.app_context():
            db.create_all()

            existing_user = (
                db.session.query(User)
                .filter(User.username == username)
                .first()
            )

            if not existing_user:

                role_object = (
                    db.session.query(Role).filter(Role.name == "Admin").first()
                )
                current_app.appbuilder.sm.add_user(
                    username, firstname, lastname, email, role_object, password
                )
                print(f"Admin user: {username} successfully created!")
            else:
                print(f"Admin user: {username} already exists!")


def main():
    fire.Fire(Magellan)

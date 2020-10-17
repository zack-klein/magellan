import os

basedir = os.path.abspath(os.path.dirname(__file__))

ENV_PREFIX = "MAGELLAN__"


# Flask configs that can/should/must be set through env vars
SQLALCHEMY_DATABASE_URI = os.getenv(
    f"{ENV_PREFIX}SQLALCHEMY_CONN_STRING", "sqlite:///db.sqlite"
)
# ""
SECRET_KEY = os.getenv(f"{ENV_PREFIX}SECRET_KEY", "You'll never guess me!")
APP_THEME = os.getenv(f"{ENV_PREFIX}APP_THEME", "flatly.css")
ELASTICSEARCH_URL = os.getenv(f"{ENV_PREFIX}ELASTICSEARCH_URL")


# Flask configs that are constant
CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"
IMG_UPLOAD_URL = "/static/uploads/"
AUTH_TYPE = 1
AUTH_ROLE_ADMIN = "Admin"
AUTH_ROLE_PUBLIC = "Public"
APP_NAME = "Magellan"

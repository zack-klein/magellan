from flask_appbuilder import AppBuilder
from flask_appbuilder.menu import Menu

from magellan.app.index import Index
from magellan.app.sec import CustomSecurityManager


appbuilder = AppBuilder(
    menu=Menu(reverse=False),
    indexview=Index,
    security_manager_class=CustomSecurityManager,
)

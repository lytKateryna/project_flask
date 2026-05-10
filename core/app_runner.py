from flask import Flask
from flask_migrate import Migrate

from core.config import settings
from core.db import db
from routers.questions import questions_bp
from routers.category import category_bp
from models import *


def init_database(app: Flask):
    db.init_app(app=app)

    migrate = Migrate()
    migrate.init_app(app, db)


def register_routes(app: Flask):
    app.register_blueprint(questions_bp)
    app.register_blueprint(category_bp)


def create_app(app: Flask) -> Flask:
    app.config.update(settings.get_flask_config())

    init_database(app)
    register_routes(app)

    return app
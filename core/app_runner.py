from flask import Flask
from core.config import settings
from routers.questions import questions_bp
from core.db import db
from flask_migrate import Migrate
from models import *


def init_database(app: Flask):
    db.init_app(app=app)

    migrate = Migrate()
    migrate.init_app(app, db)

def register_routes(app: Flask):
    app.register_blueprint(questions_bp)

def create_app(app: Flask) -> Flask:

    app.config.update(settings.get_flask_config())

    init_database(app)
    register_routes(app)

    return app
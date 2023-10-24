from flask import Flask
from app.models import db
from app.api import api
from app.extensions import jwt, cors
from config import config


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)

    config[config_name].init_app(app)
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    return app

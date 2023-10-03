from flask import Flask


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    return app

from datetime import timedelta
import os
from flask import Flask
from typing import Dict, Type

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ERROR_MESSAGE_KEY = "message"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app: Flask):
        """Initialize the Flask app with this configuration.

        Args:
            app (Flask): Flask application to initialize
        """
        app.config.from_object(cls)


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL", "sqlite:///" + os.path.join(basedir, "store-dev.db")
    )


class TestingConfig(Config):
    TESTING = True
    JWT_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", "sqlite:///" + os.path.join(basedir, "store-test.db")
    )


class ProductionConfig(Config):
    JWT_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "store.db")
    )


config: Dict[str, Type[Config]] = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

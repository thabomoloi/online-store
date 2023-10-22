from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

db = SQLAlchemy()
api = Api(prefix="/api", version="1.0", description="Online store API")

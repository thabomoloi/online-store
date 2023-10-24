from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
api = Api(prefix="/api", version="1.0", description="Online store API")
jwt = JWTManager()
cors = CORS()
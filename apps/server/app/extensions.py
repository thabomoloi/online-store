from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()

authorizations = {
    "access_token": {"type": "apiKey", "in": "header", "name": "Authorization"}
}
api = Api(
    prefix="/api",
    authorizations=authorizations,
    security="access_token",
    version="1.0",
    description="Online store API",
)
jwt = JWTManager()
cors = CORS()

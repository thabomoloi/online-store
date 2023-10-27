from app.extensions import api
from app.api import jwt_callbacks
from app.api.namespaces.auth import auth_ns


api.add_namespace(auth_ns)

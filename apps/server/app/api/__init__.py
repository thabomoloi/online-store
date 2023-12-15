from app.extensions import api
from app.api import jwt_callbacks
from app.api.namespaces.auth import auth_ns
from app.api.namespaces.users import users_ns
from app.api.namespaces.products import products_ns


api.add_namespace(auth_ns)
api.add_namespace(users_ns)
api.add_namespace(products_ns)

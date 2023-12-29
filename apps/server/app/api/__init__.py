from app.extensions import api
from app.api import jwt_callbacks
from app.api.auth.resources import auth_ns
from app.api.users.resources import users_ns
from app.api.products.resources import products_ns

api.add_namespace(auth_ns)
api.add_namespace(users_ns)
api.add_namespace(products_ns)

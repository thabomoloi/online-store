from app.extensions import api
from app.api.auth import auth_ns

api.add_namespace(auth_ns)

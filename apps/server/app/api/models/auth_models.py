from flask_restx import Model, fields
from .. import api


parent = api.model(
    "Parent", {"name": fields.String, "class": fields.String(discriminator=True)}
)

child = api.inherit("Child", parent, {"extra": fields.String})
base_model = lambda x, y: api.inherit(
    y,
    child,
    {
        "code": fields.Integer(example=x),
        "description": fields.String,
    },
    doc=False,
)
login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, example="john.doe@example.com"),
        "password": fields.String(required=True, example="password123", doc=True),
    },
)

token_model = api.model(
    "Token", {"jwt_access_token": fields.String, "jwt_refresh_token": fields.String}
)
profile_model = api.model(
    "Profile",
    {
        "name": fields.String(
            example="John Doe", description="The name of the current user."
        ),
        "email": fields.String(
            example="john.doe@example.com", description="The email of the current user."
        ),
    },
)

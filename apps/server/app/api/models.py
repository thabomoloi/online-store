from flask_restx import Model, fields, Resource
from app.api import api


login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, example="john.doe@example.com"),
        "password": fields.String(required=True, example="password123"),
    },
)


token_model = api.model(
    "Tokens",
    {
        "jwt_access_token": fields.String(required=True),
        "jwt_refresh_token": fields.String,
    },
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

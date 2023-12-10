from flask_restx import fields
from app.api import api
from .base_models import base_user_model

signup_model = base_user_model.extend(
    "Signup",
    {
        "password": fields.String(required=True, example="password123", description="Password of the user."),
    }
)

login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, example="john.doe@example.com", description="Email of the user."),
        "password": fields.String(required=True, example="password123", description="Password of the user."),
    },
)

token_model = api.model(
    "Tokens",
    {
        "jwt_access_token": fields.String(required=True, desciption="JWT Access Token"),
        "jwt_refresh_token": fields.String(description="JWT Refresh Token"),
    },
)

authenticated_model = api.model(
    "Authenticated", 
    {
        "is_authenticated": fields.Boolean(
            required=True,
            example=False,
            description="Login status of the current user. True if JWT token sent with request else false."
        )
    }
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

# Register the models
api.models[signup_model.name] = signup_model
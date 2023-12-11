from flask_restx import fields
from app.api import api
from .base_models import base_user_model, response_model

signup_model = base_user_model.clone(
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

token_response_model = response_model.clone(
    "Token Response",
    {
        "data":   fields.Nested( api.model(
            "Tokens",
            {
                "access_token": fields.String(description="JWT Access Token"),
                "refresh_token": fields.String(description="JWT Refresh Token"),
            },
        )
        ),
    }
)


is_authenticated_response_model = response_model.clone(
    "Authenticated Reponse", 
    {
        "data": fields.Nested(api.model(
            "Authenticated", {
                "is_authenticated": fields.Boolean(
                    required=True,
                    example=False,
                    description="Login status of the current user. True if valid JWT token sent with request else false.",
                )
            })
        )
    },
)

profile_response_model = response_model.clone(
    "Profile Response",
    {
        "data": fields.Nested(api.model(
            "Profile",
            {
                "name": fields.String(example="John Doe", description="The name of the current user."),
                "email": fields.String(example="john.doe@example.com", description="The email of the current user."),
            },
        ))
    }
)

# Register the models
models = [is_authenticated_response_model, profile_response_model, signup_model, token_response_model]
for model in models:
    api.models[model.name] = model
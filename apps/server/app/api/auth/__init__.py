"""Contains parsers and models associated with `auth` namespace resources"""

from flask_restx import fields, reqparse

from app.api import api

"""
    REQUEST PARSERS
"""

login_parser = reqparse.RequestParser()
login_parser.add_argument(name="email", required=True, type=str, location="json")
login_parser.add_argument(name="password", required=True, type=str, location="json")

signup_parser = reqparse.RequestParser()
signup_parser.add_argument(name="first_name", required=True, type=str, location="json")
signup_parser.add_argument(name="last_name", required=True, type=str, location="json")
signup_parser.add_argument(name="email", required=True, type=str, location="json")
signup_parser.add_argument(name="phone", required=False, type=str, location="json")
signup_parser.add_argument(name="password", required=True, type=str, location="json")


"""
    MODELS
"""
token_model = api.model(
    "Tokens",
    {
        "access_token": fields.String(description="JWT Access Token"),
        "refresh_token": fields.String(description="JWT Refresh Token"),
    },
)


is_authenticated_model = api.model(
    "Authenticated",
    {
        "is_authenticated": fields.Boolean(
            required=True,
            example=False,
            description="Login status of the current user. True if valid JWT token sent with request else false.",
        )
    },
)

profile_model = api.model(
    "Profile",
    {
        "name": fields.String(
            example="John Doe", description="The name of the current user."
        ),
        "email": fields.String(
            example="john.doe@example.com",
            description="The email of the current user.",
        ),
    },
)

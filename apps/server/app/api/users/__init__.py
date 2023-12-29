"""Contains parsers and models associated with `users` namespace resources"""

from flask_restx import fields
from app.api import api
from app.models.users import Role

"""
    MODELS
"""

user_model = api.model(
    "User",
    {
        "id": fields.String(
            required=True,
            description="The unique identifier for the user.",
            readonly=True,
            example="89e9e1b2-e586-4788-8fbb-3307c432c18f",
        ),
        "first_name": fields.String(
            required=True, description="The first name of the user.", example="John"
        ),
        "last_name": fields.String(
            required=True, description="The last name of the user.", example="Doe"
        ),
        "email": fields.String(
            required=True,
            description="The email of the user.",
            example="john.doe@example.com",
        ),
        "phone": fields.String(
            description="The phone number of the user. This field can be null.",
            example="0712345689",
        ),
        "role": fields.String(
            description="The role of the user",
            enum=[role.value for role in Role],
            example="Administrator",
            default="Customer",
            required=True,
            readonly=True,
        ),
    },
)

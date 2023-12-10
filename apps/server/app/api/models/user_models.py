from flask_restx import fields
from app.api import api
from app.models.users import Role
from .base_models import base_user_model

user_model = base_user_model.extend(
    "User",
    {
        "id": fields.String(
            required=True,
            description="The unique identifier for the user.",
            readonly=True,
            example="89e9e1b2-e586-4788-8fbb-3307c432c18f",
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

api.models[user_model.name] = user_model
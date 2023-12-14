from flask_restx import fields
from app.api import api
from app.models.users import Role
from .base_models import base_user_model, response_model

user_model = base_user_model.clone(
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

user_response_model = response_model.clone(
    "User Response", {"data": fields.Nested(user_model)}
)

user_list_response_model = response_model.clone(
    "User List Response", {"data": fields.List(fields.Nested(user_model))}
)

# Register the models
models = [user_model, user_response_model, user_list_response_model]
for model in models:
    api.models[model.name] = model

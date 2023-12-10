from flask_restx import fields
from app.api import api

base_user_model = api.model(
    "Base User Model", 
    {
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
    }
)
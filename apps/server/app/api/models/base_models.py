from flask_restx import fields, Model
from app.api import api


base_user_model = Model(
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


error_model = api.model(
    "Error Response", 
    {
        "code": fields.Integer(required=True, description="The HTTP status code."),
        "description": fields.String(required=True, description="The short description about the response."),
        "message": fields.String(required=True, description="The error message.")
    }
)


response_model = api.model(
    "Response",
    {
        "code": fields.Integer(required=True, description="The HTTP status code.", example=200),
        "description": fields.String(required=True, description="The short description about the response.", example="Success"),
        "message": fields.String(description="Optional response message.")     
    }
)

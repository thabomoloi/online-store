from email.policy import default
from flask_restx import Model, fields, Resource
from app.api import api
from app.models.users import Role


########## Models for auth ############
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
            enum=[role.name for role in Role],
            example="Administrator",
            default="Customer",
            required=True,
        ),
    },
)


address_model = api.model(
    "Address",
    {
        "id": fields.String(
            description="The unique identifier for the address.",
            readonly=True,
            example="89e9e1b2-e586-4788-8fbb-3307c432c18f",
            required=True,
        ),
        "recipient_name": fields.String(
            description="The name of the recipient at the address.",
            example="John Doe",
            required=True,
        ),
        "recipient_phone": fields.String(
            required=True,
            description="The phone number of the recipient.",
            example="0712345689",
        ),
        "street": fields.String(
            required=True,
            description="The street address.",
            example="123 Main St",
        ),
        "suburb": fields.String(
            description="The suburb. This field can be null.", example="Some Suburb"
        ),
        "city": fields.String(
            required=True,
            description="The city or town.",
            example="Flask City",
        ),
        "postal_code": fields.String(
            required=True,
            description="The postal code or ZIP code",
            example="1234",
        ),
    },
)

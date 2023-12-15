from flask_restx import fields
from app.api import api
from .base_models import response_model


rating_model = api.model(
    "Rating",
    {
        "rate": fields.Integer(
            required=True,
            description="Average ratings of a product. The default is 0 if no ratings yet.",
            example=3.75,
            default=0,
        ),
        "count": fields.Integer(
            requird=True,
            description="The number of the ratings. The default is 0 if no ratings yet.",
            example=267,
            default=0,
        ),
    },
)

product_model = api.model(
    "Product",
    {
        "id": fields.String(
            required=True,
            readonly=True,
            description="The unique identifier for the product.",
            example="e26a44aa-4683-4a45-85a4-b2f65112d5ed",
        ),
        "code": fields.String(
            required=True, description="The unique product code.", example="P01234"
        ),
        "name": fields.String(description="The name of the product", example="Eggs"),
        "image": fields.String(
            description="The url of the product's image",
            example="/static/images/products/eggs.jpg",
        ),
        "description": fields.String(description="The description of the product"),
        "price": fields.Integer(
            description="The price of the product (in cents).", example=12999
        ),
        "stock": fields.Integer(
            required=True, description="The available stock of the product", example=500
        ),
        "category_id": fields.String(
            decription="The unique identifier for the category the product belongs to.",
            example="d3a4f975-eb44-4e1c-8e9c-3be0c6314c91",
        ),
        "rating": fields.Nested(rating_model),
    },
)

product_response_model = response_model.clone(
    "Product Response Model", {"data": fields.Nested(product_model)}
)

product_list_response_model = response_model.clone(
    "Product List Response Model", {"data": fields.List(fields.Nested(product_model))}
)

category_model = api.model(
    "Category",
    {
        "id": fields.String(
            required=True,
            readonly=True,
            description="The unique identifier for the category.",
            example="e26a44aa-4683-4a45-85a4-b2f65112d5ed",
        ),
        "name": fields.String(description="The name of the category."),
    },
)

category_response_model = response_model.clone(
    "Category Response", {"data": fields.Nested(category_model)}
)

category_list_response_model = response_model.clone(
    "Category List Response", {"data": fields.List(fields.Nested(category_model))}
)

review_model = api.model(
    "Review",
    {
        "id": fields.String(
            required=True,
            readonly=True,
            description="The unique identifier for the review.",
            example="e26a44aa-4683-4a45-85a4-b2f65112d5ed",
        ),
        "rate": fields.Integer(
            required=True, description="The rating of a product", example=5
        ),
        "comment": fields.String(description="The comment about the product"),
        "date": fields.Date(
            required=True,
            description="The date of the review in YYYY-MM-DD format.",
            example="2023-12-15",
        ),
        "product_id": fields.String(
            required=True,
            description="The unique identifier for the product being reviewed.",
            example="e26a44aa-4683-4a45-85a4-b2f65112d5ed",
        ),
        "user_id": fields.String(
            required=True,
            description="The unique identifier for the user reviewing the product.",
            example="e26a44aa-4683-4a45-85a4-b2f65112d5ed",
        ),
    },
)

review_response_model = response_model.clone(
    "Review Response", {"data": fields.Nested(review_model)}
)

review_list_response_model = response_model.clone(
    "Review List Response", {"data": fields.List(fields.Nested(review_model))}
)

# Register the models
models = [
    product_response_model,
    product_list_response_model,
    category_response_model,
    category_list_response_model,
    review_response_model,
    review_list_response_model,
]
for model in models:
    api.models[model.name] = model

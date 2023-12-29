"""Contains parsers and models associated with `products` namespace resources"""

from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.api import api


"""
    REQUEST PARSERS
"""
product_parser = reqparse.RequestParser()
product_parser.add_argument(name="code", required=True, type=str, location="form")
product_parser.add_argument(name="name", required=True, type=str, location="form")
product_parser.add_argument(
    name="image",
    required=False,
    type=FileStorage,
    location="files",
)
product_parser.add_argument(
    name="description",
    required=True,
    type=str,
    location="form",
)
product_parser.add_argument(name="price", required=True, type=int, location="form")
product_parser.add_argument(name="stock", required=True, type=int, location="form")


"""
    MODELS
"""
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

product_image_model = api.model(
    "Product Image",
    {
        "id": fields.String(
            required=True,
            readonly=True,
            description="The unique identifier for the product.",
            example="e26a44aa-4683-4a45-85a4-b2f65112d5ed",
        ),
        "default": fields.Boolean(
            description="Boolean field to represent whether the image is the default product image"
        ),
        "url": fields.String(
            description="The url of the product's image",
            example="/static/images/products/eggs.jpg",
        ),
        "product_id": fields.String(
            description="The unique identifier for the product.",
            example="e26a44aa-4683-4a45-85a4-b2f65112d5ed",
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
        "images": fields.List(fields.Nested(product_image_model)),
        "rating": fields.Nested(rating_model),
    },
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

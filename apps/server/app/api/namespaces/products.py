from http import HTTPStatus
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, marshal

from app.api.models.base_models import error_model
from app.api.models.product_models import (
    category_model,
    category_response_model,
    category_list_response_model,
    product_model,
    product_response_model,
    product_list_response_model,
    review_model,
    review_response_model,
    review_list_response_model,
)
from app.api.namespaces import create_response
from app.models import db, Product, Category, Review

products_ns = Namespace("products", description="Operations related to products")


@products_ns.route("/products")
@products_ns.response(
    code=HTTPStatus.UNAUTHORIZED.value,
    description=HTTPStatus.UNAUTHORIZED.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.NOT_FOUND.value,
    description=HTTPStatus.NOT_FOUND.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
    description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
    model=error_model,
)
class ProductListResource(Resource):
    @products_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=product_list_response_model,
    )
    def get(self):
        """Get a list of all products."""
        response = create_response(
            code=200,
            description="Success",
            message=None,
            data=marshal(Product.query.all(), product_model),
        )
        return response, response["code"]


@products_ns.route("/products/<string:id>")
@products_ns.doc(params={"id": "The unique identifier for the product."})
@products_ns.response(
    code=HTTPStatus.UNAUTHORIZED.value,
    description=HTTPStatus.UNAUTHORIZED.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.NOT_FOUND.value,
    description=HTTPStatus.NOT_FOUND.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
    description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
    model=error_model,
)
class ProductResource(Resource):
    @products_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=product_response_model,
    )
    def get(self, id: str):
        product: Product = Product.query.get(id)
        if product is None:
            status = HTTPStatus.NOT_FOUND
            response = create_response(
                code=status.value,
                description=status.phrase,
                message="The requested product cannot be found.",
            )
        else:
            status = HTTPStatus.OK
            response = create_response(
                code=status.value,
                description=status.phrase,
                message=None,
                data=marshal(product, product_model),
            )
        return response, response["code"]


@products_ns.route("/categories")
@products_ns.response(
    code=HTTPStatus.UNAUTHORIZED.value,
    description=HTTPStatus.UNAUTHORIZED.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.NOT_FOUND.value,
    description=HTTPStatus.NOT_FOUND.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
    description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
    model=error_model,
)
class CategoryListResource(Resource):
    @products_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=category_list_response_model,
    )
    def get(self):
        """Get a list of all categories."""
        response = create_response(
            code=200,
            description="Success",
            message=None,
            data=marshal(Category.query.all(), category_model),
        )
        return response, response["code"]


@products_ns.route("/categories/<string:id>")
@products_ns.doc(params={"id": "The unique identifier for the category."})
@products_ns.response(
    code=HTTPStatus.UNAUTHORIZED.value,
    description=HTTPStatus.UNAUTHORIZED.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.NOT_FOUND.value,
    description=HTTPStatus.NOT_FOUND.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
    description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
    model=error_model,
)
class CategoryResource(Resource):
    @products_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=category_response_model,
    )
    def get(self, id: str):
        category: Category = Category.query.get(id)
        if category is None:
            status = HTTPStatus.NOT_FOUND
            response = create_response(
                code=status.value,
                description=status.phrase,
                message="The requested category cannot be found.",
            )
        else:
            status = HTTPStatus.OK
            response = create_response(
                code=status.value,
                description=status.phrase,
                message=None,
                data=marshal(category, category_model),
            )
        return response, response["code"]


@products_ns.route("/reviews")
@products_ns.response(
    code=HTTPStatus.UNAUTHORIZED.value,
    description=HTTPStatus.UNAUTHORIZED.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.NOT_FOUND.value,
    description=HTTPStatus.NOT_FOUND.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
    description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
    model=error_model,
)
class ReviewListResource(Resource):
    @products_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=review_list_response_model,
    )
    def get(self):
        """Get a list of all reviews."""
        response = create_response(
            code=200,
            description="Success",
            message=None,
            data=marshal(Review.query.all(), review_model),
        )
        return response, response["code"]


@products_ns.route("/reviews/<string:id>")
@products_ns.doc(params={"id": "The unique identifier for the review."})
@products_ns.response(
    code=HTTPStatus.UNAUTHORIZED.value,
    description=HTTPStatus.UNAUTHORIZED.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.NOT_FOUND.value,
    description=HTTPStatus.NOT_FOUND.phrase,
    model=error_model,
)
@products_ns.response(
    code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
    description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
    model=error_model,
)
class ReviewResource(Resource):
    @products_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=review_response_model,
    )
    def get(self, id: str):
        review: Review = Review.query.get(id)
        if review is None:
            status = HTTPStatus.NOT_FOUND
            response = create_response(
                code=status.value,
                description=status.phrase,
                message="The requested review cannot be found.",
            )
        else:
            status = HTTPStatus.OK
            response = create_response(
                code=status.value,
                description=status.phrase,
                message=None,
                data=marshal(review, review_model),
            )
        return response, response["code"]

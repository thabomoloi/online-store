import os
from typing import List

from flask import request, session, url_for
from config import basedir
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, abort

from werkzeug.datastructures import FileStorage

from app.api.products import category_model, product_model, review_model, product_parser
from app.api.utils import create_error_responses
from app.extensions import photos
from app.models import db, Product, Category, Review, ProductImage

products_ns = Namespace("products", description="Operations related to products")


@products_ns.route("/products")
class ProductListResource(Resource):
    @products_ns.doc("list_all_products")
    @products_ns.marshal_list_with(product_model)
    def get(self):
        """Get a list of all products."""
        return Product.query.all()

    @products_ns.doc("all_new_product")
    @products_ns.expect(product_parser)
    @products_ns.marshal_with(product_model)
    def post(self):
        """Create a new product."""

        args = product_parser.parse_args()

        try:
            images: List[FileStorage] = args.pop("images", None)
            product = Product(**args)
            product_images = []
            for image in images:
                filename = photos.save(image, "products")
                url = photos.url(filename)
                product_images.append(ProductImage(url=url, product=product))

            db.session.add_all([product, *product_images])
            db.session.commit()
            return product

        except Exception as e:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


@products_ns.route("/products/<string:id>")
@products_ns.doc(params={"id": "The unique identifier for the product."})
class ProductResource(Resource):
    @products_ns.doc("get_product")
    @products_ns.marshal_with(product_model)
    def get(self, id: str):
        """Get a product"""
        product: Product = Product.query.get(id)
        if product is None:
            abort(HTTPStatus.NOT_FOUND)
        return product

    @products_ns.doc("update_product")
    def put(self, id: str):
        """Update a product"""
        product: Product = Product.query.get(id)
        if product is None:
            abort(HTTPStatus.NOT_FOUND)

    @products_ns.doc("delete_product")
    @products_ns.response(
        code=HTTPStatus.NO_CONTENT.value, description=HTTPStatus.NO_CONTENT.phrase
    )
    def delete(self, id: str):
        """delete a product"""
        product: Product = Product.query.get(id)
        if product is None:
            abort(HTTPStatus.NOT_FOUND)
        try:
            db.session.delete(product)
            db.session.commit()
            return "", HTTPStatus.NO_CONTENT
        except:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@products_ns.route("/categories")
class CategoryListResource(Resource):
    @products_ns.marshal_list_with(category_model)
    def get(self):
        """Get a list of all categories."""
        return Category.query.all()


@products_ns.route("/categories/<string:id>")
@products_ns.doc(params={"id": "The unique identifier for the category."})
class CategoryResource(Resource):
    @products_ns.marshal_with(category_model)
    def get(self, id: str):
        category: Category = Category.query.get(id)
        if category is None:
            abort(HTTPStatus.NOT_FOUND)
        return category


@products_ns.route("/reviews")
class ReviewListResource(Resource):
    @products_ns.marshal_list_with(review_model)
    def get(self):
        """Get a list of all reviews."""
        return Review.query.all()


@products_ns.route("/reviews/<string:id>")
@products_ns.doc(params={"id": "The unique identifier for the review."})
class ReviewResource(Resource):
    @products_ns.marshal_with(review_model)
    def get(self, id: str):
        review: Review = Review.query.get(id)
        if review is None:
            abort(HTTPStatus.NOT_FOUND)
        return review


# document the error responses
error_responses = create_error_responses(products_ns)
resources = [
    ProductListResource,
    ProductResource,
    CategoryListResource,
    CategoryResource,
    ReviewListResource,
    ReviewResource,
]
for error_response in error_responses:
    for resource in resources:
        error_response(resource)

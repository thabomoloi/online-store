from flask_restx import reqparse

from werkzeug.datastructures import FileStorage

product_parser = reqparse.RequestParser()
product_parser.add_argument(name="code", required=True, type=str, location="files")
product_parser.add_argument(name="name", required=True, type=str, location="files")
product_parser.add_argument(
    name="image", required=True, type=FileStorage, location="files"
)
product_parser.add_argument(
    name="description", required=True, type=str, location="files"
)
product_parser.add_argument(name="price", required=True, type=int, location="files")
product_parser.add_argument(name="stock", required=True, type=int, location="files")

# reqparse.Argument()

from http import HTTPStatus
from flask_restx import Namespace, fields

from app.api import api

message_model = api.model("Message", {"message": fields.String})


def make_error_response(namespace: Namespace, status=HTTPStatus.INTERNAL_SERVER_ERROR):
    return namespace.response(
        code=status.value, description=status.phrase, model=message_model
    )


def create_error_responses(namespace: Namespace):
    http_error_statuses = [
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.UNAUTHORIZED,
        HTTPStatus.NOT_FOUND,
        HTTPStatus.UNPROCESSABLE_ENTITY,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    ]
    return list(
        map(lambda status: make_error_response(namespace, status), http_error_statuses)
    )

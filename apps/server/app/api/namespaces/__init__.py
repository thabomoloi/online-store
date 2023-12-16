from http import HTTPStatus
from typing import Any, Dict

from flask_restx import Namespace

from app.api.models.base_models import error_model


def create_response(
    code: int, description: str, message, data: Any = None
) -> Dict[str, Any]:
    response = {"code": code, "description": description, "message": message}
    if data is not None:
        response["data"] = data
    return response


def make_error_response(namespace: Namespace, status=HTTPStatus.INTERNAL_SERVER_ERROR):
    return namespace.response(
        code=status.value, description=status.phrase, model=error_model
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

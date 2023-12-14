from http import HTTPStatus
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, marshal

from app.models import db
from app.models.users import User
from app.api.models.base_models import error_model
from app.api.models.user_models import (
    user_model,
    user_response_model,
    user_list_response_model,
)
from app.api.namespaces import create_response

users_ns = Namespace("users", description="Operations for users")


@users_ns.route("/users")
class UsersListResource(Resource):
    @jwt_required()
    @users_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=user_list_response_model,
    )
    @users_ns.response(
        code=HTTPStatus.UNAUTHORIZED.value,
        description=HTTPStatus.UNAUTHORIZED.phrase,
        model=error_model,
    )
    @users_ns.response(
        code=HTTPStatus.NOT_FOUND.value,
        description=HTTPStatus.NOT_FOUND.phrase,
        model=error_model,
    )
    @users_ns.response(
        code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
        description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
        model=error_model,
    )
    def get(self):
        response = create_response(
            code=200,
            description="Success",
            message=None,
            data=marshal(User.query.all(), user_model),
        )
        return response, response["code"]


@users_ns.route("/users/<string:id>")
@users_ns.doc(params={"id": "The unique identifier for the user."})
class UsersResource(Resource):
    @jwt_required()
    @users_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=user_response_model,
    )
    @users_ns.response(
        code=HTTPStatus.UNAUTHORIZED.value,
        description=HTTPStatus.UNAUTHORIZED.phrase,
        model=error_model,
    )
    @users_ns.response(
        code=HTTPStatus.NOT_FOUND.value,
        description=HTTPStatus.NOT_FOUND.phrase,
        model=error_model,
    )
    @users_ns.response(
        code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
        description=HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
        model=error_model,
    )
    def get(self, id: str):
        user: User = User.query.get(id)
        if user is None:
            status = HTTPStatus.NOT_FOUND
            response = create_response(
                code=status.value,
                description=status.phrase,
                message="The requested user cannot be found.",
            )
        else:
            status = HTTPStatus.OK
            response = create_response(
                code=status.value,
                description=status.phrase,
                message=None,
                data=marshal(user, user_model),
            )
        return response, response["code"]

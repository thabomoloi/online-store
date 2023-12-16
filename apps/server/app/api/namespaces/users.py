from http import HTTPStatus
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, marshal

from app.models import db
from app.models.users import User
from app.api.models.user_models import (
    user_model,
    user_response_model,
    user_list_response_model,
)
from app.api.namespaces import create_error_responses, create_response

users_ns = Namespace("users", description="Operations related to users")


@users_ns.route("/users")
class UsersListResource(Resource):
    @jwt_required()
    @users_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=user_list_response_model,
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


# document the error responses
error_responses = create_error_responses(users_ns)
resources = [UsersResource, UsersListResource]
for error_response in error_responses:
    for resource in resources:
        error_response(resource)

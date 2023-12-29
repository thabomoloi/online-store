from http import HTTPStatus
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, abort, marshal

from app.models import db, User

from app.api.users import user_model
from app.api.utils import create_error_responses

users_ns = Namespace("users", description="Operations related to users")


@users_ns.route("/users")
class UsersListResource(Resource):
    @jwt_required()
    @users_ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()


@users_ns.route("/users/<string:id>")
@users_ns.doc(params={"id": "The unique identifier for the user."})
class UsersResource(Resource):
    @jwt_required()
    @users_ns.marshal_with(user_model)
    def get(self, id: str):
        user: User = User.query.get(id)
        if user is None:
            abort(HTTPStatus.NOT_FOUND, "The requested user cannot be found.")
        return user


# document the error responses
error_responses = create_error_responses(users_ns)
resources = [UsersResource, UsersListResource]
for error_response in error_responses:
    for resource in resources:
        error_response(resource)

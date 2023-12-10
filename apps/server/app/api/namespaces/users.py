from flask_restx import Namespace, Resource

from app.models import db
from app.models.users import User
from app.api.models.user_models import user_model

users_ns = Namespace("users", description="Operations for users")


@users_ns.route("/users")
class UsersListResource(Resource):
    @users_ns.marshal_list_with(user_model, envelope="users")
    def get(self):
        return User.query.all()


@users_ns.route("/users/<string:id>")
@users_ns.doc(params={"id": "The unique identifier for the user."})
class UsersResource(Resource):
    @users_ns.marshal_with(user_model, envelope="user")
    def get(self, id: str):
        user: User = User.query.get(id)
        if user is None:
            return {"msg": "The requested user cannot be found."}
        return user

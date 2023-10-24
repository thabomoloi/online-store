from flask import jsonify, request
from flask_cors import cross_origin
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)

from app.extensions import jwt, cors
from app.models.users import User

auth_ns = Namespace("auth", description="Operations for authentication")


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    """Callback function that takes in the `User` object as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Callback function that loads a user from your database whenever
    a protected route is accessed.
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@auth_ns.route("/login")
class LoginResource(Resource):
    def post(self):
        email = "john.doe@example.com"
        password = "password123"
        user: User = User.query.filter_by(email=email).one_or_none()
        if not user or not user.verify_password(password):
            return {"msg": "Invalid login"}, 401

        response = jsonify({"msg": "Login successful"})
        access_token = create_access_token(identity=user)
        set_access_cookies(response, access_token)
        csrf_access_token = request.cookies.get("csrf_access_token")

        return response


@auth_ns.route("/logout")
class LogoutResource(Resource):
    def post(self):
        response = jsonify({"msg": "Logout successful"})
        unset_jwt_cookies(response)
        return response

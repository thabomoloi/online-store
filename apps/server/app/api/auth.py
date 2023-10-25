from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from .models.auth_models import login_model, profile_model, token_model
from app.extensions import jwt
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
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_model, envelope="data")
    def post(self):
        """Log in to the server."""
        email: str = auth_ns.payload.get("email")
        password: str = auth_ns.payload.get("password")
        user: User = User.query.filter_by(email=email).one_or_none()
        if not user or not user.verify_password(password):
            return {"message": "Invalid login"}, 401

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        # create_access_token(identity, fresh=datetime.timedelta(minutes=15))

        return dict(jwt_access_token=access_token, jwt_refresh_token=refresh_token)


@auth_ns.route("/refresh")
@jwt_required(refresh=True)
class RefreshTokenResource(Resource):
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return dict(jwt_access_token=access_token)

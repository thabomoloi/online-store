from datetime import datetime, timezone, timedelta
from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt,
    jwt_required,
)

from .models.auth_models import (
    login_model,
    profile_model,
    token_model,
)
from app.extensions import jwt
from app.models import db
from app.models.users import User
from app.models.auth import TokenBlocklist

auth_ns = Namespace("auth", description="Operations for authentication")


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    """Callback function that takes in the `User` object as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data) -> User | None:
    """Callback function that loads a user from your database whenever
    a protected route is accessed.
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    """Callback function to check if a JWT exists in the database blocklist."""
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_model, envelope="tokens", skip_none=True)
    def post(self):
        """Log in to the server."""
        email: str = auth_ns.payload.get("email")
        password: str = auth_ns.payload.get("password")
        user: User = User.query.filter_by(email=email).one_or_none()
        if not user or not user.verify_password(password):
            return {"message": "Invalid login"}, 401

        access_token = create_access_token(identity=user, fresh=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=user)

        return dict(jwt_access_token=access_token, jwt_refresh_token=refresh_token)


@auth_ns.route("/logout")
class LogoutResource(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
        db.session.commit()
        return jsonify(message=f"{ttype.capitalize()} token successfully revoked")


@auth_ns.route("/refresh")
@auth_ns.header("Authorization")
class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    @auth_ns.marshal_with(token_model, envelope="tokens", skip_none=True)
    @auth_ns.doc(security="access_token")
    def post(self):
        """Refresh the access token"""
        access_token = create_access_token(identity=get_current_user(), fresh=False)
        return dict(jwt_access_token=access_token)

from datetime import datetime, timezone, timedelta
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt,
    jwt_required,
)

from app.models import db
from app.models.users import User
from app.models.auth import TokenBlocklist

from app.api.models import (
    login_model,
    profile_model,
    token_model,
)


auth_ns = Namespace("auth", description="Operations for authentication")


@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_model, envelope="tokens", skip_none=True)
    def post(self):
        """Log in"""
        email: str = auth_ns.payload.get("email")
        password: str = auth_ns.payload.get("password")
        user: User = User.query.filter_by(email=email).one_or_none()
        if not user or not user.verify_password(password):
            return dict(msg="Invalid login"), 401

        access_token = create_access_token(identity=user, fresh=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=user)

        return dict(jwt_access_token=access_token, jwt_refresh_token=refresh_token)


@auth_ns.route("/logout")
class LogoutResource(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        """Log out"""
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
        db.session.commit()
        return dict(msg=f"{ttype.capitalize()} token successfully revoked")


@auth_ns.route("/refresh")
@auth_ns.header("Authorization")
class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    @auth_ns.marshal_with(token_model, envelope="tokens", skip_none=True)
    def post(self):
        """Refresh the access token"""
        access_token = create_access_token(identity=get_current_user(), fresh=False)
        return dict(jwt_access_token=access_token)


@auth_ns.route("/details")
class DetailsResource(Resource):
    @jwt_required()
    @auth_ns.marshal_with(profile_model)
    def get(self):
        """Get current user's name and email."""
        user: User = get_current_user()
        return dict(
            name=f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
            email=user.email,
        )

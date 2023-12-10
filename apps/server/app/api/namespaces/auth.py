from datetime import datetime, timezone, timedelta
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_jwt,
    jwt_required,
)

from app.models import db
from app.models.users import User
from app.models.auth import TokenBlocklist


from app.api.models.auth_models import (
    authenticated_model, 
    login_model,
    profile_model,
    signup_model, 
    token_model, 
)

from sqlalchemy.exc import IntegrityError

auth_ns = Namespace("auth", description="Operations for authentication")


@auth_ns.route("/signup")
class SignupResource(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        keys = ["first_name", "last_name", "email", "phone", "password"]
        details = dict(list(map(lambda key: (key, auth_ns.payload.get(key)),keys)))
        user = User(**details)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return dict(msg="The email already exists"), 400
        return dict(msg="Account created successfully")
    
    
@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_model, envelope="tokens", skip_none=True)
    @auth_ns.response(401, description="Unauthorized")
    def post(self):
        """Log in"""
        email: str = auth_ns.payload.get("email")
        password: str = auth_ns.payload.get("password")
        user: User = User.query.filter_by(email=email).one_or_none()
        if not user or not user.verify_password(password):
            return dict(msg="Invalid login"), 401

        refresh_token = create_refresh_token(identity=user)
        refresh_token_jti = decode_token(refresh_token)["jti"]
        access_token = create_access_token(
            identity=user,
            fresh=timedelta(minutes=15),
            additional_claims={"refresh_jti": refresh_token_jti},
        )

        return dict(jwt_access_token=access_token, jwt_refresh_token=refresh_token)


@auth_ns.route("/logout")
class LogoutResource(Resource):
    @jwt_required()
    def delete(self):
        """Log out"""
        token = get_jwt()
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=token["jti"], type="access", created_at=now))
        db.session.add(
            TokenBlocklist(jti=token["refresh_jti"], type="refresh", created_at=now)
        )
        db.session.commit()
        return dict(msg=f"Tokens successfully revoked")


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
    @auth_ns.marshal_with(profile_model, envelope="user")
    def get(self):
        """Get current user's name and email."""
        user: User = get_current_user()
        return dict(
            name=f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
            email=user.email,
        )

@auth_ns.route("/is-authenticated")
class IsAuthenticatedResource(Resource):
    @jwt_required(optional=True)
    @auth_ns.marshal_with(authenticated_model)
    def get(self):
        """Check if the current user is authenticated."""
        user: User = get_current_user()
        return dict(is_authenticated=(user is not None))
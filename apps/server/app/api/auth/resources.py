from datetime import timedelta, timezone
import datetime
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_jwt,
    jwt_required,
)
from sqlalchemy.exc import IntegrityError
from flask_restx import Namespace, Resource, abort
from app.api.auth import (
    login_parser,
    signup_parser,
    token_model,
    profile_model,
    is_authenticated_model,
)
from app.api.utils import create_error_responses, message_model
from app.exceptions import EmailExistsExcepton, NullPasswordException
from app.models import db, User, TokenBlocklist


auth_ns = Namespace("auth", description="Operations for authentication")


@auth_ns.route("/signup")
class SignupResource(Resource):
    @auth_ns.expect(signup_parser)
    @auth_ns.marshal_with(message_model)
    def post(self):
        """Create new user account"""
        args = signup_parser.parse_args()

        try:
            user = User(**args)
            db.session.add(user)
            db.session.commit()
            return dict(message="You have successful created an account")
        except EmailExistsExcepton:
            db.session.rollback()
            abort(
                HTTPStatus.BAD_REQUEST,
                "The email you used already exists. Please login or use a different email address.",
            )
        except (IntegrityError, NullPasswordException):
            db.session.rollback()
            abort(HTTPStatus.BAD_REQUEST, "Missing required data.")
        except:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_parser)
    @auth_ns.marshal_with(token_model)
    def post(self):
        """Log in"""
        args = login_parser.parse_args()
        email: str = args.get("email")
        password: str = args.get("password")

        user: User = User.query.filter_by(email=email).one_or_none()

        if not user or not user.verify_password(password):
            abort(HTTPStatus.UNAUTHORIZED)

        refresh_token = create_refresh_token(identity=user)
        refresh_token_jti = decode_token(refresh_token)["jti"]
        access_token = create_access_token(
            identity=user,
            fresh=timedelta(minutes=15),
            additional_claims={"refresh_jti": refresh_token_jti},
        )

        return dict(access_token=access_token, refresh_token=refresh_token)


@auth_ns.route("/logout")
class LogoutResource(Resource):
    @jwt_required()
    @auth_ns.response(
        code=HTTPStatus.NO_CONTENT.value, description=HTTPStatus.NO_CONTENT.phrase
    )
    def delete(self):
        """Log out"""
        token = get_jwt()
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=token["jti"], type="access", created_at=now))
        db.session.add(
            TokenBlocklist(jti=token["refresh_jti"], type="refresh", created_at=now)
        )
        try:
            db.session.commit()
        except:
            db.session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)


@auth_ns.route("/refresh")
class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    @auth_ns.marshal_with(token_model)
    def post(self):
        """Refresh the access token"""
        access_token = create_access_token(identity=get_current_user(), fresh=False)
        return dict(jwt_access_token=access_token)


@auth_ns.route("/profile")
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


@auth_ns.route("/is-authenticated")
class IsAuthenticatedResource(Resource):
    @jwt_required(optional=True)
    @auth_ns.marshal_with(is_authenticated_model)
    def get(self):
        """Check if the current user is authenticated."""
        user: User = get_current_user()
        return dict(is_authenticated=(user is not None))


# document the error responses
error_responses = create_error_responses(auth_ns)

resources = [
    SignupResource,
    LoginResource,
    LogoutResource,
    RefreshTokenResource,
    DetailsResource,
    IsAuthenticatedResource,
]
for error_response in error_responses:
    for resource in resources:
        error_response(resource)

from datetime import datetime, timezone, timedelta
from http import HTTPStatus
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


from app.api.models.base_models import response_model
from app.api.models.auth_models import (
    is_authenticated_response_model,
    profile_response_model,
    token_response_model,
)

from sqlalchemy.exc import IntegrityError

from app.api.namespaces import create_response, create_error_responses
from app.api.parsers.auth import login_parser, signup_parser
from app.exceptions import EmailExistsExcepton, NullPasswordException

auth_ns = Namespace("auth", description="Operations for authentication")


@auth_ns.route("/signup")
class SignupResource(Resource):
    @auth_ns.expect(signup_parser)
    @auth_ns.response(
        code=HTTPStatus.CREATED.value,
        description=HTTPStatus.CREATED.phrase,
        model=response_model,
    )
    def post(self):
        """Create new user account"""
        args = signup_parser.parse_args()
        try:
            user = User(**args)
            db.session.add(user)
            db.session.commit()
            response = create_response(
                code=HTTPStatus.CREATED.value,
                description=HTTPStatus.CREATED.phrase,
                message="Your account was created successfully.",
            )
        except EmailExistsExcepton:
            db.session.rollback()
            response = create_response(
                code=HTTPStatus.BAD_REQUEST.value,
                description=HTTPStatus.BAD_REQUEST.phrase,
                message="The email address you used already exists. Please login or use a different email address.",
            )
        except (IntegrityError, NullPasswordException):
            db.session.rollback()
            response = create_response(
                code=HTTPStatus.BAD_REQUEST.value,
                description=HTTPStatus.BAD_REQUEST.phrase,
                message="Missing some required data.",
            )
        except:
            db.session.rollback()
            response = create_response(
                code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                description=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                message="Oops! Something went wrong.",
            )
        finally:
            return response, response["code"]


@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_parser)
    @auth_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=token_response_model,
    )
    def post(self):
        """Log in"""
        args = login_parser.parse_args()
        email: str = args.get("email")
        password: str = args.get("password")
        user: User = User.query.filter_by(email=email).one_or_none()

        if not user or not user.verify_password(password):
            response = create_response(
                code=HTTPStatus.UNAUTHORIZED.value,
                description=HTTPStatus.UNAUTHORIZED.phrase,
                message="Invalid login. Your email or password is incorrect.",
            )
            return response, response["code"]

        refresh_token = create_refresh_token(identity=user)
        refresh_token_jti = decode_token(refresh_token)["jti"]
        access_token = create_access_token(
            identity=user,
            fresh=timedelta(minutes=15),
            additional_claims={"refresh_jti": refresh_token_jti},
        )

        response = create_response(
            code=HTTPStatus.OK.value,
            description=HTTPStatus.OK.phrase,
            message="Your login was successful.",
            data=dict(access_token=access_token, refresh_token=refresh_token),
        )

        return response, response["code"]


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
            response = create_response(
                code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                description=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                message="Oops! Something went wrong.",
            )
            return response, response["code"]


@auth_ns.route("/refresh")
class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    @auth_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=token_response_model,
    )
    def post(self):
        """Refresh the access token"""
        access_token = create_access_token(identity=get_current_user(), fresh=False)
        response = create_response(
            code=HTTPStatus.OK.value,
            description=HTTPStatus.OK.phrase,
            message=None,
            data=dict(jwt_access_token=access_token),
        )
        return response, response["code"]


@auth_ns.route("/profile")
class DetailsResource(Resource):
    @jwt_required()
    @auth_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=profile_response_model,
    )
    def get(self):
        """Get current user's name and email."""
        user: User = get_current_user()
        response = create_response(
            code=HTTPStatus.OK.value,
            description=HTTPStatus.OK.phrase,
            message=None,
            data=dict(
                name=f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
                email=user.email,
            ),
        )
        return response, response["code"]


@auth_ns.route("/is-authenticated")
class IsAuthenticatedResource(Resource):
    @jwt_required(optional=True)
    @auth_ns.response(
        code=HTTPStatus.OK.value,
        description=HTTPStatus.OK.phrase,
        model=is_authenticated_response_model,
    )
    def get(self):
        """Check if the current user is authenticated."""
        user: User = get_current_user()
        response = create_response(
            code=HTTPStatus.OK.value,
            description=HTTPStatus.OK.phrase,
            message=None,
            data=dict(is_authenticated=(user is not None)),
        )
        return response, response["code"]


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

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


from app.api.models.base_models import error_model, response_model
from app.api.models.auth_models import (
    is_authenticated_response_model,
    login_model,
    profile_response_model,
    signup_model, 
    token_response_model
)

from sqlalchemy.exc import IntegrityError

from app.api.namespaces import create_response

auth_ns = Namespace("auth", description="Operations for authentication")


@auth_ns.route("/signup")
class SignupResource(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.response(code=201, description="Account created", model=response_model)
    @auth_ns.response(code=400, description="Bad request", model=error_model)
    def post(self):
        keys = ["first_name", "last_name", "email", "phone", "password"]
        details = dict(list(map(lambda key: (key, auth_ns.payload.get(key)),keys)))
        user = User(**details)
        db.session.add(user)

        try:
            db.session.commit()
            response = create_response(
                code=201, 
                description="Account created", 
                message="Your account was created successfully."
            )
        except IntegrityError:
            db.session.rollback()
            response = create_response(
                code=400, 
                description="Bad request", 
                message="The email address you used already exists. Please login or use a different email address."
            ) 
        return response, response["code"]
    

@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(code=200, description="Success", model=token_response_model)
    @auth_ns.response(code=401, description="Unauthorized", model=error_model)
    def post(self):
        """Log in"""
        email: str = auth_ns.payload.get("email")
        password: str = auth_ns.payload.get("password")
        user: User = User.query.filter_by(email=email).one_or_none()
        
        if not user or not user.verify_password(password):
            response = create_response(
                code=401,
                description="Unauthorized",
                message="Invalid login. Your email or password is incorrect."
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
            code=200,
            description="Success",
            message="Your login was successful.",
            data=dict(access_token=access_token, refresh_token=refresh_token)
        ) 
        
        return response, response["code"]


@auth_ns.route("/logout")
class LogoutResource(Resource):
    @jwt_required()
    @auth_ns.response(code=204, description="", model=response_model)
    @auth_ns.response(code=401, description="Unauthorized", model=error_model)
    @auth_ns.response(code=500, description="Internal Server Error", model=error_model)
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
            response = create_response(
                code=204,
                description="",
                message="You have logged out successfully."
            )
        except:
            db.session.rollback()
            response = create_response(
                code=500,
                description="Internal Server Error",
                message="Oops! Something went wrong."
            )
        return response, response["code"]


@auth_ns.route("/refresh")
class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    @auth_ns.response(code=200, description="Success", model=token_response_model)
    @auth_ns.response(code=401, description="Unauthorized", model=error_model)
    def post(self):
        """Refresh the access token"""
        access_token = create_access_token(identity=get_current_user(), fresh=False)
        response = create_response(
            code=200,
            description="Success",
            message=None,
            data=dict(jwt_access_token=access_token)
        )
        return response, response["code"]


@auth_ns.route("/profile")
class DetailsResource(Resource):
    @jwt_required()
    @auth_ns.response(code=200, description="Success", model=profile_response_model)
    @auth_ns.response(code=401, description="Unauthorized", model=error_model)
    def get(self):
        """Get current user's name and email."""
        user: User = get_current_user()
        response = create_response(
            code=200,
            description="Success",
            message=None,
            data=dict(
                name=f"{user.first_name.capitalize()} {user.last_name.capitalize()}",
                email=user.email,
            )
        )
        return response, response["code"]


@auth_ns.route("/is-authenticated")
class IsAuthenticatedResource(Resource):
    @jwt_required(optional=True)
    @auth_ns.response(code=200, description="Success", model=is_authenticated_response_model)
    def get(self):
        """Check if the current user is authenticated."""
        user: User = get_current_user()
        response = create_response(
            code=200,
            description="Success",
            message=None,
            data=dict(is_authenticated=(user is not None))
        )
        return response, response["code"]
    
    

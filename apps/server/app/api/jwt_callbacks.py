from http import HTTPStatus
from flask import jsonify
from flask_jwt_extended.config import config
from flask.typing import ResponseReturnValue
from app.extensions import jwt
from app.models import db
from app.models.users import User
from app.models.auth import TokenBlocklist


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    """Callback function that takes in the `User` object as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(jwt_header: dict, jwt_data: dict) -> User | None:
    """Callback function that loads a user from your database whenever
    a protected route is accessed.
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header: dict, jwt_payload: dict) -> bool:
    """Callback function to check if a JWT exists in the database blocklist."""
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@jwt.invalid_token_loader
def invalid_token_callback(error_string: str) -> ResponseReturnValue:
    """
    By default, if an invalid token attempts to access a protected endpoint, we
    return the error string for why it is not valid with a 422 status code

    :param error_string: String indicating why the token is invalid
    """
    status = HTTPStatus.UNPROCESSABLE_ENTITY
    return (
        jsonify({"code": status.value , "description": status.phrase, "message": error_string}), 
        status
    )

@jwt.unauthorized_loader
def unauthorized_callback(error_string: str) -> ResponseReturnValue:
    """
    By default, if a protected endpoint is accessed without a JWT, we return
    the error string indicating why this is unauthorized, with a 401 status code

    :param error_string: String indicating why this request is unauthorized
    """
    
    status = HTTPStatus.UNAUTHORIZED
    return (
        jsonify({"code": status.value , "description": status.phrase, "message": error_string}), 
        status
    )
    
@jwt.expired_token_loader
def expired_token_callback(_expired_jwt_header: dict, _expired_jwt_data: dict) -> ResponseReturnValue:
    """
    By default, if an expired token attempts to access a protected endpoint,
    we return a generic error message with a 401 status
    """
    status = HTTPStatus.UNAUTHORIZED
    return (
        jsonify({"code": status.value , "description": status.phrase, "message": "Token has expired"}), 
        status
    )

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header: dict, jwt_data: dict) -> ResponseReturnValue:
    """
    By default, if a non-fresh jwt is used to access a ```fresh_jwt_required```
    endpoint, we return a general error message with a 401 status code
    """
    status = HTTPStatus.UNAUTHORIZED
    return (
        jsonify({"code": status.value , "description": status.phrase, "message": "Fresh token required"}), 
        status
    )
    
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header: dict, jwt_data: dict) -> ResponseReturnValue:
    """
    By default, if a revoked token is used to access a protected endpoint, we
    return a general error message with a 401 status code
    """
    status = HTTPStatus.UNAUTHORIZED
    return (
        jsonify({"code": status.value , "description": status.phrase, "message": "Token has been revoked"}), 
        status
    )

@jwt.user_lookup_error_loader
def user_lookup_error_callback(_jwt_header: dict, jwt_data: dict) -> ResponseReturnValue:
    """
    By default, if a user_lookup callback is defined and the callback
    function returns None, we return a general error message with a 401
    status code
    """
    identity = jwt_data[config.identity_claim_key]
    status = HTTPStatus.UNAUTHORIZED
    return (
        jsonify({"code": status.value , "description": status.phrase, "message": f"Error loading the user {identity}"}), 
        status
    )

@jwt.token_verification_failed_loader
def token_verification_failed_callback(_jwt_header: dict, _jwt_data: dict) -> ResponseReturnValue:
    """
    By default, if the user claims verification failed, we return a generic
    error message with a 400 status code
    """
    status = HTTPStatus.BAD_REQUEST
    return (
        jsonify({"code": status.value , "description": status.phrase, "message": "User claims verification failed"}), 
        status
    )

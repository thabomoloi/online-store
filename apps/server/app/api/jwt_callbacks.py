from app.extensions import jwt
from app.models import db
from app.models.users import User
from app.models.auth import TokenBlocklist


@jwt.user_identity_loader
def user_identity_lookup(user: User):
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

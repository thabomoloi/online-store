"""Module for defining the tables related to users of the application"""
import uuid
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import NoReturn
from enum import Enum


class Role(Enum):
    Guest = "Guest"
    Customer = "Customer"
    Moderator = "Moderator"
    Administrator = "Administrator"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16), nullable=True)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.Customer)
    password_hash = db.Column(db.String(255), name="password", nullable=False)
    addresses = db.relationship("Address", backref="user", lazy=True)
    cart = db.relationship("Cart", uselist=False, backref="user", lazy=True)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def __init__(self, **kwargs) -> None:
        super(User, self).__init__(**kwargs)

    @property
    def password(self) -> NoReturn:
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifies user's password by checking if the stored
        password hash matches the given password.

        Args:
            password (str): The password to verify

        Returns:
            bool: True if the given password matches the password_hash, else returns False
        """
        return check_password_hash(self.password_hash, password)


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    receipient_name = db.Column(db.String(255), nullable=False)
    receipient_phone = db.Column(db.String(16), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    suburb = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs) -> None:
        super(Address, self).__init__(**kwargs)

    def formatted(self) -> str:
        """Converts the current Address object to one line separated by commas."""
        address_attributes = [
            self.street,
            self.suburb,
            self.city,
            self.postal_code,
        ]
        address_attributes = list(filter(lambda x: x is not None, address_attributes))
        return ", ".join(address_attributes)

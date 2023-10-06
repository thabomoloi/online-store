"""Module for defining the tables related to users of the application"""
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16), nullable=True)
    password_hash = db.Column(db.String(255), name="password", nullable=False)

    def __init__(self, **kwargs) -> None:
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    receipient_name = db.Column(db.String(255), nullable=False)
    receipient_phone = db.Column(db.String(16), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    suburb = db.Column(db.String(255))
    city = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)

    def to_oneline(self):
        address_attributes = [
            self.street,
            self.suburb,
            self.city,
            self.postal_code,
        ]
        return ", ".join(address_attributes)

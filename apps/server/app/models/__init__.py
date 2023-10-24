"""A subpackage for defining database tables for the application"""
from app.extensions import db

from app.models.users import User
from app.models.cart import Cart
from app.models.products import Review
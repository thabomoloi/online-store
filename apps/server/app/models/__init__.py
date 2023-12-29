"""A subpackage for defining database tables for the application"""
from app.extensions import db

from app.models.auth import TokenBlocklist
from app.models.users import User, Address
from app.models.cart import Cart, CartItem
from app.models.products import Review, Product, Category, ProductImage

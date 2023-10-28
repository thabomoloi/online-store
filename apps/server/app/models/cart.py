import uuid
from app.models import db


class Cart(db.Model):
    __tablename__ = "carts"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cart_items = db.relationship("CartItem", backref="cart", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)

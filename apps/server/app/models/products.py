from typing import Dict
import uuid

from sqlalchemy import func
from app.models import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL")
    )
    reviews = db.relationship("Review", backref="product", lazy=True)

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @property
    def rating(self) -> Dict[str, int]:
        count = len(self.reviews)
        ratings_sum = (
            db.session.query(func.sum(Review.rate))
            .filter_by(product_id=self.id)
            .scalar()
        )
        rate = 0 if ratings_sum is None else round(ratings_sum / count, 2)
        return dict(rate=rate, count=count)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(255))
    products = db.relationship("Product", backref="category", lazy=True)

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs):
        super(Review, self).__init__(**kwargs)

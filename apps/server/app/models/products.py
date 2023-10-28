import uuid
from app.models import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id", ondelete="SET NULL")
    )
    reviews = db.relationship("Review", backref="product", lazy=True)

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    @property
    def average_ratings(self):
        count = 0
        avg_rating = 0
        for review in self.reviews:
            count += 1
            avg_rating += review.rating

        if count > 0:
            return round(avg_rating / count, 2)
        return 0

    @property
    def reviews_count(self):
        return len(self.reviews)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    products = db.relationship("Product", backref="category", lazy=True)

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, **kwargs):
        super(Review, self).__init__(**kwargs)

from app.models.users import User
from tests import BaseTestCase
from app.models import db
from app.models.products import Product, Category, Review
from sqlalchemy.exc import IntegrityError


class ProductsBaseTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
        )
        db.session.add(self.user)
        db.session.commit()


class TestCategoryModel(BaseTestCase):
    def test_category_model(self):
        category = Category(name="Test Category")
        db.session.add(category)
        db.session.commit()

        retrieved_category = (
            db.session.query(Category).filter_by(name="Test Category").first()
        )
        self.assertIsNotNone(retrieved_category)

    def test_category_model_null_data(self):
        category = Category()
        db.session.add(category)
        with self.assertRaises(IntegrityError):
            db.session.commit()


class TestReviewModel(ProductsBaseTestCase):
    def test_review_model(self):
        product = Product(
            code="ABC123",
            name="Test Product",
            description="This is a test product",
            price=10.0,
            stock=100,
        )
        review = Review(
            rate=5, comment="Great product", product=product, user_id=self.user.id
        )
        db.session.add(review)
        db.session.commit()

        self.assertIsNotNone(product.id)
        self.assertIsNotNone(review.id)
        self.assertIn(review, product.reviews)
        db.session.commit()

    def test_review_model_null_data(self):
        review = Review()
        db.session.add(review)
        with self.assertRaises(IntegrityError):
            db.session.commit()


class TestProductModel(ProductsBaseTestCase):
    def test_product_model(self):
        product = Product(
            code="ABC123",
            name="Test Product",
            description="This is a test product",
            price=10.0,
            stock=100,
            category_id=None,
        )
        db.session.add(product)
        db.session.commit()

        retrieved_product = db.session.query(Product).filter_by(code="ABC123").first()
        self.assertIsNotNone(retrieved_product)
        if retrieved_product:
            self.assertEqual(retrieved_product.name, "Test Product")
            self.assertEqual(retrieved_product.ratings["rate"], 0)  # No reviews added
            self.assertEqual(retrieved_product.ratings["count"], 0)

    def test_product_model_null_data(self):
        product = Product()
        db.session.add(product)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_assign_product_to_category(self):
        category = Category(name="Test Category")
        product = Product(
            code="ABC123",
            name="Test Product",
            description="This is a test product",
            price=10.0,
            stock=100,
            category=category,
        )

        db.session.add(product)
        db.session.commit()

        self.assertIsNotNone(category.id)
        self.assertIsNotNone(product.id)
        self.assertEqual(category.id, product.category_id)
        self.assertIn(product, category.products)

    def test_product_reviews(self):
        product = Product(
            code="ABC123",
            name="Test Product",
            description="This is a test product",
            price=10.0,
            stock=100,
        )
        reviews = [
            Review(rate=5, comment="Great product", user_id=self.user.id),
            Review(rate=3, comment="It's okay", user_id=self.user.id),
            Review(rate=2, comment="Bad product", user_id=self.user.id),
        ]
        for review in reviews:
            product.reviews.append(review)
        db.session.add(product)
        db.session.commit()

        self.assertEqual(product.ratings["count"], 3)
        self.assertEqual(round((5 + 3 + 2) / 3, 2), product.ratings["rate"])

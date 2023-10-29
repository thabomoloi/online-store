from app.models.products import Product
from app.models.users import User
from tests import BaseTestCase
from app.models import db
from app.models.cart import Cart, CartItem
from sqlalchemy.exc import IntegrityError


class CartBaseTestCase(BaseTestCase):
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


class TestCartModel(CartBaseTestCase):
    def test_create_cart(self):
        cart = Cart()
        cart.user_id = self.user.id
        db.session.add(cart)
        db.session.commit()
        self.assertIsNotNone(cart.id)

    def test_create_cart_no_user(self):
        cart = Cart()
        db.session.add(cart)
        with self.assertRaises(IntegrityError):
            db.session.commit()


class TestCartItemModel(CartBaseTestCase):
    def test_create_cart_item(self):
        cart = Cart()
        cart.user_id = self.user.id

        product = Product(
            code="ABC123",
            name="Test Product",
            description="This is a test product",
            price=10.0,
            stock=100,
        )

        db.session.add(product)
        db.session.add(cart)
        db.session.commit()

        cart_item = CartItem()
        cart_item.product_id = product.id
        cart_item.quantity = 4
        cart_item.cart_id = cart.id

        db.session.add(cart_item)
        db.session.commit()
        self.assertIsNotNone(cart_item.id)

    def test_create_cart_item_null_data(self):
        cart_item = CartItem()
        db.session.add(cart_item)
        with self.assertRaises(IntegrityError):
            db.session.commit()

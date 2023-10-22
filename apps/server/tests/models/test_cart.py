from app.models.products import Product
from tests import BaseTestCase
from app.models import db
from app.models.cart import Cart, CartItem
from sqlalchemy.exc import IntegrityError

class TestCartModel(BaseTestCase):
    def test_create_cart(self):
        cart = Cart()
        cart.user_id = self.user.id;
        db.session.add(cart)
        db.session.commit()
        self.assertIsNotNone(cart.id)
        
    def test_create_cart_no_user(self):
        cart = Cart()
        db.session.add(cart)
        with self.assertRaises(IntegrityError):
            db.session.commit()
            
class TestCartItemModel(BaseTestCase):
    def test_create_cart_item(self):
        cart = Cart()
        cart.user_id = self.user.id;
        
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
        
from tests import BaseTestCase
from app.models import db
from app.models.users import User, Role, Address
from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_create_user(self):
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role=Role.Administrator,
        )

        self.assertIsNone(user.id)
        self.assertTrue(user.first_name == "John")
        self.assertTrue(user.last_name == "Doe")
        self.assertTrue(user.email == "john.doe@example.com")
        self.assertIsNone(user.phone)
        self.assertTrue(user.role == Role.Administrator)
        self.assertIsNone(user.password_hash)

    def test_password_setter(self):
        user = User(password="password123")
        self.assertIsNotNone(user.password_hash)

    def test_password_not_readable(self):
        user = User(password="password123")
        with self.assertRaises(AttributeError):
            user.password

    def test_verify_password(self):
        user = User(password="password123")
        self.assertTrue(user.verify_password("password123"))
        self.assertFalse(user.verify_password("password321"))

    def test_random_password_salts(self):
        user1 = User(password="password123")
        user2 = User(password="password123")
        self.assertFalse(user1.password_hash == user2.password_hash)

    def test_add_user_data_not_null(self):
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
        )

        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)

    def test_add_user_data_null(self):
        user = User()
        db.session.add(user)
        with self.assertRaises(IntegrityError):
            db.session.commit()


class TestAddressModel(BaseTestCase):
    def test_create_address(self):
        address = Address(
            receipient_name="John Doe",
            receipient_phone="0123456789",
            street="123 Street",
            suburb="Suburb",
            city="City",
            postal_code="1234",
        )

        self.assertIsNone(address.id)
        self.assertTrue(address.receipient_name == "John Doe")
        self.assertTrue(address.receipient_phone == "0123456789")
        self.assertTrue(address.street == "123 Street")
        self.assertTrue(address.suburb == "Suburb")
        self.assertTrue(address.city == "City")
        self.assertTrue(address.postal_code == "1234")

    def test_address_oneline(self):
        address1 = Address(
            street="123 Street",
            suburb="Suburb",
            city="City",
            postal_code="1234",
        )
        self.assertTrue(address1.formatted() == "123 Street, Suburb, City, 1234")

        address2 = Address(
            street="123 Street",
            city="City",
            postal_code="1234",
        )
        self.assertTrue(address2.formatted() == "123 Street, City, 1234")

    def test_add_address_data_not_null(self):
        address = Address(
            receipient_name="John Doe",
            receipient_phone="0123456789",
            street="123 Street",
            suburb="Suburb",
            city="City",
            postal_code="1234",
            user_id=self.user.id,
        )
        db.session.add(address)
        db.session.commit()

        self.assertIsNotNone(address.id)

    def test_add_address_data_null(self):
        address = Address()
        db.session.add(address)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_assign_address_to_user(self):
        address = Address(
            receipient_name="John Doe",
            receipient_phone="0123456789",
            street="123 Street",
            suburb="Suburb",
            city="City",
            postal_code="1234",
        )
        address.user = User(  # type: ignore
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role=Role.Administrator,
            password="password123",
        )

        db.session.add(address)
        db.session.commit()

        self.assertIsNotNone(address.id)
        self.assertIsNotNone(address.user_id)

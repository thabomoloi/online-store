from tests import BaseTestCase
from app.models.user import User


class TestUserModel(BaseTestCase):
    def test_create_user(self):
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
        )

        assert user.password_hash is None
        assert user.verify_password("password123") is False

        user.password = "password123"
        assert user.password_hash is not None
        assert user.verify_password("password123")

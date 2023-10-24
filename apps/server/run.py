import os
from dotenv import load_dotenv
from flask import Flask
from app.models import db, User
from app import create_app

load_dotenv()

config_name: str = os.environ.get("CONFIG") or "default"
app: Flask = create_app(config_name)


@app.cli.command()
def test() -> None:
    """Run the unit tests."""
    import pytest

    result_code = pytest.main(["-v", "tests"])
    if result_code != 0:
        raise SystemExit(result_code)


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                password="password123",
            )
        db.session.add(user)
        db.session.commit()
    app.run(debug=True)

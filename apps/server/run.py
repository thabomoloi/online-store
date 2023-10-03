import os
from dotenv import load_dotenv
from flask import Flask

from app import create_app

load_dotenv()

config_name: str = os.environ.get("CONFIG") or "default"
app: Flask = create_app(config_name)


@app.cli.command()
def pick():
    print("ehh")
    app.app_context().push()


@app.cli.command()
def test() -> None:
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    app.run(debug=True)

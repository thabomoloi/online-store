import os
from dotenv import load_dotenv
from flask import Flask

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
    app.run(debug=True)

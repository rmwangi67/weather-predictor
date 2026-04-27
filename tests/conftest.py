import pytest
from app import app


@pytest.fixture
def client():
    """A test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def runner():
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
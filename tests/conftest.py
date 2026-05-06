"""
Shared test fixtures and configuration for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Returns a FastAPI TestClient for the application.
    """
    return TestClient(app)

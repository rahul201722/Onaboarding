"""
Test configuration for the application.
"""
import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def app():
    """Create application for testing."""
    from app import create_app
    app = create_app('testing')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

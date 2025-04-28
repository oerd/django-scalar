"""
Pytest configuration file for django-scalar tests.
"""

import pytest
from django.test import Client


@pytest.fixture
def client():
    """Return a Django test client instance."""
    return Client()

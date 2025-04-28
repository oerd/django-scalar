"""
URL patterns for testing django-scalar.
"""

from django.urls import path, include

PREFIX = "scalar"

urlpatterns = [
    path(f"{PREFIX}/", include("django_scalar.urls")),
]

"""
Tests for the URLs configuration.
"""

from django.urls import reverse, resolve

from django_scalar.views import scalar_viewer


class TestUrls:
    """Tests for the URLs configuration."""

    def test_scalar_viewer_url_resolves(self):
        """Test that the scalar_viewer URL resolves to the scalar_viewer view."""
        url = reverse("django_scalar:docs")
        assert resolve(url).func == scalar_viewer

    def test_scalar_viewer_url_name(self):
        """Test that the scalar_viewer URL name is correct."""
        from tests.urls import PREFIX

        url = reverse("django_scalar:docs")
        assert url == f"/{PREFIX}/api/docs/"

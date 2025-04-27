"""
Tests for the views module.
"""

import pytest
from django.test import RequestFactory
from django.urls import reverse
from bs4 import BeautifulSoup

from django_scalar.views import scalar_viewer


@pytest.mark.django_db
class TestScalarViewer:
    """Tests for the scalar_viewer view function."""

    def test_scalar_viewer_returns_200(self, client):
        """Test that `scalar_viewer` returns a 200 status code."""
        url = reverse("django_scalar:docs")
        response = client.get(url)
        assert response.status_code == 200

    def test_scalar_viewer_uses_correct_template(self, client):
        """Test that `scalar_viewer` uses the correct template."""
        url = reverse("django_scalar:docs")
        response = client.get(url)
        assert "django_scalar/scalar.html" in [t.name for t in response.templates]

    def test_scalar_viewer_context(self):
        """Test that `scalar_viewer` passes the correct context to the template."""
        request = RequestFactory().get("/")
        response = scalar_viewer(request)

        # Check that the context contains the expected variables
        assert "openapi_url" in response.context_data
        assert "title" in response.context_data
        assert "scalar_js_url" in response.context_data
        assert "scalar_proxy_url" in response.context_data
        assert "scalar_favicon_url" in response.context_data

        # Check the values of the context variables
        assert response.context_data["openapi_url"] == "/api/schema/"
        assert response.context_data["title"] == "Scalar Api Reference"
        assert (
            response.context_data["scalar_js_url"]
            == "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
        )
        assert response.context_data["scalar_proxy_url"] == ""
        assert response.context_data["scalar_favicon_url"] == "/static/favicon.ico"

    def test_html_content_contains_context_data(self, client):
        """Test that the HTML content contains the expected context data."""
        url = reverse("django_scalar:docs")
        response = client.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Check that the title is correctly set
        assert soup.title.string == "Scalar Api Reference"

        # Check that the favicon link is correctly set
        favicon_link = soup.find("link", rel="shortcut icon")
        assert favicon_link["href"] == "/static/favicon.ico"

        # Check that the API reference script has the correct data attributes
        api_reference_script = soup.find("script", id="api-reference")
        assert api_reference_script["data-url"] == "/api/schema/"
        assert api_reference_script["data-proxy-url"] == ""

        # Check that the scalar JS script has the correct source
        scalar_js_script = soup.find_all("script")[-1]  # Last script tag
        assert (
            scalar_js_script["src"]
            == "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
        )

    def test_html_structure_integrity(self, client):
        """Test the overall structure and integrity of the HTML document."""
        url = reverse("django_scalar:docs")
        response = client.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Check basic HTML structure
        assert soup.html["lang"] == "en"
        assert soup.head is not None
        assert soup.body is not None

        # Check for required meta tags
        meta_charset = soup.find("meta", charset="utf-8")
        assert meta_charset is not None

        meta_viewport = soup.find("meta", attrs={"name": "viewport"})
        assert meta_viewport is not None
        assert "width=device-width" in meta_viewport["content"]

        # Check for noscript message
        noscript = soup.find("noscript")
        assert noscript is not None
        assert "Scalar requires Javascript" in noscript.text

        # Check for CSS link
        css_link = soup.find("link", rel="stylesheet")
        assert css_link is not None

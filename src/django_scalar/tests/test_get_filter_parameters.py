"""
Tests for the get_filter_parameters module.
"""

from django.db import models
from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    BooleanFilter,
    DateFilter,
    ChoiceFilter,
)
from drf_spectacular.utils import OpenApiParameter

from django_scalar.get_filter_parameters import get_filter_parameters


class MockModel(models.Model):
    """A mock model for filter tests."""

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        app_label = "test_app"


class MockFilterSet(FilterSet):
    """A mock FilterSet for testing get_filter_parameters."""

    name = CharFilter(lookup_expr="iexact")
    age = NumberFilter()
    is_active = BooleanFilter()
    created_at = DateFilter()

    class Meta:
        model = MockModel
        fields = ["name", "age", "is_active", "created_at"]


class MockFilterSetWithChoices(FilterSet):
    """A mock FilterSet with choices for testing get_filter_parameters."""

    status = ChoiceFilter(
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("pending", "Pending"),
        ]
    )

    class Meta:
        model = MockModel
        fields = ["status"]


class TestGetFilterParameters:
    """Tests for the get_filter_parameters function."""

    def test_get_filter_parameters_returns_list(self):
        """Test that get_filter_parameters returns a list of OpenApiParameter objects."""
        parameters = get_filter_parameters(MockFilterSet)
        assert isinstance(parameters, list)
        assert all(isinstance(param, OpenApiParameter) for param in parameters)

    def test_get_filter_parameters_correct_count(self):
        """Test that get_filter_parameters returns the correct number of parameters."""
        parameters = get_filter_parameters(MockFilterSet)
        assert len(parameters) == 4  # name, age, is_active, created_at

    def test_get_filter_parameters_names(self):
        """Test that get_filter_parameters returns parameters with the correct names."""
        parameters = get_filter_parameters(MockFilterSet)
        parameter_names = [param.name for param in parameters]
        assert "name" in parameter_names
        assert "age" in parameter_names
        assert "is_active" in parameter_names
        assert "created_at" in parameter_names

    def test_get_filter_parameters_types(self):
        """Test that get_filter_parameters returns parameters with the correct types."""
        parameters = get_filter_parameters(MockFilterSet)

        # Find parameters by name
        name_param = next(param for param in parameters if param.name == "name")
        age_param = next(param for param in parameters if param.name == "age")
        is_active_param = next(
            param for param in parameters if param.name == "is_active"
        )
        created_at_param = next(
            param for param in parameters if param.name == "created_at"
        )

        # Check types
        assert name_param.type is str
        assert age_param.type is int
        assert is_active_param.type is bool
        assert created_at_param.type is str

    def test_get_filter_parameters_descriptions(self):
        """Test that get_filter_parameters returns parameters with the correct descriptions."""
        parameters = get_filter_parameters(MockFilterSet)

        # Find parameters by name
        name_param = next(param for param in parameters if param.name == "name")

        # Check description
        assert "case-insensitive" in name_param.description

    def test_get_filter_parameters_with_choices(self):
        """Test that get_filter_parameters correctly handles ChoiceFilter."""
        parameters = get_filter_parameters(MockFilterSetWithChoices)

        # Find status parameter
        status_param = next(param for param in parameters if param.name == "status")

        # Check enum values
        assert status_param.enum == ["active", "inactive", "pending"]

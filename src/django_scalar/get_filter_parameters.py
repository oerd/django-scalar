from typing import Type, List, Optional

from django_filters import FilterSet
from django_filters.filters import (
    NumberFilter,
    DateFilter,
    BooleanFilter,
    ChoiceFilter,
    ModelChoiceFilter,
)
from drf_spectacular.utils import OpenApiParameter
from rest_framework.fields import DecimalField


def get_filter_parameters(
    filter_class: Type[FilterSet],
) -> Optional[List[OpenApiParameter]]:
    """
    Automatically generate OpenAPI parameters from a FilterSet class.

    Args:
        filter_class: The FilterSet class to generate parameters from

    Returns:
        List of OpenApiParameter objects
    """
    parameters = []

    for field_name, filter_instance in filter_class().filters.items():
        parameter_type = str  # default type
        enum = None

        # Determine parameter type based on filter type
        if isinstance(filter_instance, NumberFilter):
            parameter_type = (
                float if isinstance(filter_instance.field, DecimalField) else int
            )
        elif isinstance(filter_instance, BooleanFilter):
            parameter_type = bool
        elif isinstance(filter_instance, DateFilter):
            parameter_type = str
        elif isinstance(filter_instance, ChoiceFilter):
            parameter_type = str
            enum = [choice[0] for choice in filter_instance.extra["choices"]]
        elif isinstance(filter_instance, ModelChoiceFilter):
            parameter_type = int
            description = (
                f"ID of related {filter_instance.field.queryset.model.__name__}"
            )

        # Get lookup expression for description
        lookup_expr = getattr(filter_instance, "lookup_expr", "exact")

        # Build description
        if lookup_expr == "icontains":
            description = f"Filter by {field_name} (case-insensitive, partial match)"
        elif lookup_expr == "gte":
            description = f"Filter by {field_name} (greater than or equal)"
        elif lookup_expr == "lte":
            description = f"Filter by {field_name} (less than or equal)"
        elif lookup_expr == "iexact":
            description = f"Filter by exact {field_name} (case-insensitive)"
        else:
            description = f"Filter by {field_name}"

        # Create parameter
        param = OpenApiParameter(
            name=field_name,
            type=parameter_type,
            location="query",
            description=description,
            required=False,
            enum=enum,
        )

        parameters.append(param)
    return parameters

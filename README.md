# Django Scalar

Django-Scalar provides an easy way to serve your API docs with [Scalar](https://scalar.com).

> **Note**: This project is still in its early stages. Pull requests are welcome.

## Installation

The python package to install is `django-scalar`. You can install it with `pip install django-scalar`
or `uv add django-scalar` based on your preferred python package manager.

## Integrate in your Django app

At this stage, the view expects that you have your OpenAPI schema published
with `DRF-Spectacular` under the `api/schema/` endpoint. See below under **Customize
Django Scalar** for how you can customize this.

To integrate django scalar include `django-scalar.views.scalar_viewer` in your `urls.py`.

```python
from django.urls import path
from django_scalar.views import scalar_viewer
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    # ...existing URL patterns...
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Add this:
    path("api-docs/", scalar_viewer, name="scalar-viewer"),
]
```

Feel free to change `api-docs/` to your liking. We've seen `api/docs` etc. in the wild.

## Customize Django Scalar

> ℹ️ **Note** we have plans to make this easier soon.

The `scalar_viewer` view will pass on some hardcoded defaults to the template. You can
[override the template](https://docs.djangoproject.com/en/5.2/howto/overriding-templates/)
and change everything to match your environment.

## Requirements:
There are two main requirements for this project:
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- [django-filters](https://django-filter.readthedocs.io/en/stable/) (optional)

This project implicitly depends on Django and Django-Rest-Framework.

## Testing

For information on running tests, see the [tests README](tests/README.md).

## Documentation example:
```python
    #views.py
    @extend_schema(
        responses={200: UserSerializer},
        tags=["User"],
        description="Retrieve a list of all users",
        methods=["GET"],
        parameters=get_filter_parameters(UserFilter), ## this get_filter_parameters is using the django-filters base to create the necessary parameters automatically.
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)
  #filters/user.py
```
## Using `get_filter_parameters`

You need to create a basic or complex django-filter class and then use the script from
[`get_filter_parameters`](https://github.com/m1guer/django-scalar/blob/main/src/django_scalar/get_filter_parameters.py)
the auto-parse the class to a valid `OpenApiParameter`.

```python
  #(app)/filters/users.py
  import django_filters
  from django.conf import settings


  class UserFilter(django_filters.FilterSet):
      # Filter by username (case-insensitive exact match)
      username = django_filters.CharFilter(lookup_expr="iexact")

      # Filter by email (case-insensitive exact match)
      email = django_filters.CharFilter(lookup_expr="iexact")

      # Filter by full name (case-insensitive partial match)
      full_name = django_filters.CharFilter(
          field_name="first_name", lookup_expr="icontains", label="Full Name"
      )

      # Filter by is_active (boolean filter)
      is_active = django_filters.BooleanFilter()

      # Filter by date joined (range filter for datetime)
      date_joined_start = django_filters.DateTimeFilter(
          field_name="date_joined", lookup_expr="gte", label="Joined After"
      )
      date_joined_end = django_filters.DateTimeFilter(
          field_name="date_joined", lookup_expr="lte", label="Joined Before"
      )

      # Filter by genres (many-to-many relationship)
      genres = django_filters.ModelMultipleChoiceFilter(
          queryset=User.objects.all(), field_name="genres__name", label="Genres"
      )

      # Filter by trusty (boolean filter)
      is_trusty = django_filters.BooleanFilter()

      # Filter by fee range (decimal filter)
      min_fee = django_filters.NumberFilter(
          field_name="fee", lookup_expr="gte", label="Min Fee"
      )
      max_fee = django_filters.NumberFilter(
          field_name="fee", lookup_expr="lte", label="Max Fee"
      )
      type = django_filters.ChoiceFilter(
          choices=[
              ("music", "Musico"),
              ("establishment", "Estabelecimento"),
          ],
      )

      class Meta:
          model = settings.AUTH_USER_MODEL,
          fields = [
              "username",
              "email",
              "is_active",
              "is_trusty",
              "genres",
              "date_joined_start",
              "date_joined_end",
              "min_fee",
              "max_fee",
              "type",
          ]
```

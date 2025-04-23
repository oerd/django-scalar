> **Note** ⚠️ This is based on code forked from github.com/m1guer/django-scalar


## requirements:
- [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- [django-filters](https://django-filter.readthedocs.io/en/stable/) (optional)


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
## usage of get_filter_parameters
- you need to create a basic or complex django-filter class and then use the script from [get_filter_parameters](https://github.com/m1guer/django-scalar/blob/main/get_filter_parameters.py) the auto-parse the class to a valid OpenApiParameter
```python
  #(app)/filters/users.py
  import django_filters
  from core.models.user import User


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
          model = User
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

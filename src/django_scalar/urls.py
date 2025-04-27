from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import scalar_viewer


app_name = "django_scalar"

urlpatterns = [
    # Endpoint below needs to match {openapi_url} from views.scalar_viewer
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(  # FIXME: this is not needed but if you want, you can keep it.
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/docs/", scalar_viewer, name="docs"),  # scalar view.
]

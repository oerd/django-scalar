from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .scalar import scalar_viewer


app_name = "django_scalar"

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"), # im using drf_spectacular and is the one that i tested with. ps: this endpoint need to be the same from {openapi_url}
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ), # is not needed but if you want, you can keep it.
    path("api/docs/", scalar_viewer, name="docs"), # scalar view.
]

from django.shortcuts import render


def scalar_viewer(request):
    openapi_url = "/api/schema/"
    title = "Scalar Api Reference"
    scalar_js_url = "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
    scalar_proxy_url = ""
    scalar_favicon_url = "/static/favicon.ico"
    return render(request, "django_scalar/scalar.html", locals())

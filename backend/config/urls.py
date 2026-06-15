from django.contrib import admin
from django.urls import path, include
from users.views import get_profile
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/profile/<int:tg_id>/", get_profile),
    path("webapp/catalog/", TemplateView.as_view(template_name="catalog.html")),
]
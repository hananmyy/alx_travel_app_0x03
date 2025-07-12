from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from listings.views import home_view, verify_payment

# Swagger Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel API",
        default_version="v1",
        description="API documentation for ALX Travel App",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin Panel
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),  # API Docs
    path("api/", include("listings.urls")),  # API Routes
    path("", home_view, name="home"),  # Global homepage route
    path('chapa-webhook', include('django_chapa.urls')),
    path("verify-payment/<str:tx_ref>/", verify_payment),
]
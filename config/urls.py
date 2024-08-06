"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (SpectacularSwaggerView,
                                   SpectacularRedocView,
                                   SpectacularAPIView)

from config import settings
from src.users.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls, ),

    path("api/auth/", include("src.users.api_urls")),
    path("api/books/", include("src.core.api_urls")),
    path('users/', include('src.users.view_urls')),
    path('main/', include('src.core.view_urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path(
        "api/docs/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    ]
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

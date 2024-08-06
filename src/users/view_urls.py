"""
URL configuration for app users.

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
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from config import settings
from src.users.views import LoginView, RegisterLibrarianView, RegisterVisitorView

# from src.users.views import VisitorLogin, LibrarianLogin

urlpatterns = [
    path('register/visitor', RegisterVisitorView.as_view(), name='register_visitor'),
    path('register/librarian', RegisterLibrarianView.as_view(), name='register_librarian'),
    path('logout/', LogoutView.as_view(next_page='login',), name='logout'),
]
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

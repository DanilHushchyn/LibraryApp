from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    # User Auth
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="user"),

    path('', include(router.urls)),
]

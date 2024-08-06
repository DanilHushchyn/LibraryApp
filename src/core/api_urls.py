from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.core.endpoints import (BookViewSet,
                                )

router = DefaultRouter()
router.register('', BookViewSet)

urlpatterns = [

    path('', include(router.urls)),
]

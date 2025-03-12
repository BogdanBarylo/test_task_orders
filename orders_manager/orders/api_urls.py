from __future__ import annotations
from django.urls import include, path
from rest_framework import routers
from .api import OrderViewSet

router: routers.DefaultRouter = routers.DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]

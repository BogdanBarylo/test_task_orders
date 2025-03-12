from __future__ import annotations
from django.urls import path, include
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    revenue_view,
)

urlpatterns = [
    # Веб-интерфейс:
    path("", OrderListView.as_view(), name="list"),
    path("detail/<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("create/", OrderCreateView.as_view(), name="create"),
    path("update/<int:pk>/", OrderUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="delete"),
    path("revenue/", revenue_view, name="revenue"),
    # Подключение API:
    path("api/", include("orders_manager.orders.api_urls")),
]

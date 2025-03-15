from django.urls import path, include
from .views import (
    OrderListView,
    OrderDetailView,
    create_order_with_items,
    OrderUpdateView,
    OrderDeleteView,
    revenue_view,
    add_order_item,
)

urlpatterns = [
    # Веб-интерфейс:
    path("", OrderListView.as_view(), name="list"),
    path("detail/<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("create/", create_order_with_items, name="create"),
    path("update/<int:pk>/", OrderUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="delete"),
    path("add-item/<int:pk>/", add_order_item, name="add_item"),
    path("revenue/", revenue_view, name="revenue"),
    # Подключение API:
    path("api/", include("orders_manager.orders.api_urls")),
]

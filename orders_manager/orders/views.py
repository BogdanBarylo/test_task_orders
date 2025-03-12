from __future__ import annotations
from typing import Any
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.db.models import Sum
from .models import Order


class OrderListView(ListView):
    model = Order
    template_name: str = "orders/order_list.html"
    context_object_name: str = "orders"

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        table_number = self.request.GET.get("table_number")
        status = self.request.GET.get("status")
        if table_number:
            try:
                table_number_int = int(table_number)
                queryset = queryset.filter(table_number=table_number_int)
            except ValueError:
                pass
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class OrderDetailView(DetailView):
    model = Order
    template_name: str = "orders/order_detail.html"
    context_object_name: str = "order"


class OrderCreateView(CreateView):
    model = Order
    template_name: str = "orders/order_form.html"
    fields: list[str] = ["table_number", "items"]
    success_url: str = reverse_lazy("orders:list")

    def form_valid(self, form: Any) -> Any:
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    template_name: str = "orders/order_update.html"
    fields: list[str] = ["status", "items"]
    success_url: str = reverse_lazy("orders:list")


class OrderDeleteView(DeleteView):
    model = Order
    template_name: str = "orders/order_confirm_delete.html"
    success_url: str = reverse_lazy("orders:list")


def revenue_view(request: HttpRequest) -> HttpResponse:
    """
    Вычисляет общую выручку по заказам со статусом "оплачено".
    """
    revenue: float = (
        Order.objects.filter(status="paid").aggregate(
            total_revenue=Sum("total_price"))[
            "total_revenue"
        ]
        or 0
    )
    return render(request, "orders/revenue.html", {"revenue": revenue})

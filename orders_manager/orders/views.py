from typing import Any
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Order
from .forms import OrderForm, OrderItemForm, OrderItemFormSet


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


def create_order_with_items(request: HttpRequest) -> HttpResponse:
    """
    Представление для создания заказа с одновременным добавлением блюд.
    Пользователь вводит номер стола, а затем
    через inline formset добавляет блюда.
    Новый заказ создается со статусом "pending" (в ожидании).
    """
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.status = "pending"
            order.save()
            order_items = formset.save(commit=False)
            for item in order_items:
                item.order = order
                item.save()
            return redirect("orders:detail", pk=order.pk)
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()
    return render(
        request,
        "orders/order_create_with_items.html",
        {"order_form": order_form, "formset": formset},
    )


class OrderUpdateView(UpdateView):
    model = Order
    template_name: str = "orders/order_update.html"
    fields: list[str] = ["status"]
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
        Order.objects.filter(status="paid").
        aggregate(total_revenue=Sum("total_price"))[
            "total_revenue"
        ]
        or 0
    )
    return render(request, "orders/revenue.html", {"revenue": revenue})


def add_order_item(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Представление для добавления блюда к уже созданному заказу.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect("orders:detail", pk=order.pk)
    else:
        form = OrderItemForm()
    return render(
        request, "orders/order_item_form.html", {"form": form, "order": order}
    )

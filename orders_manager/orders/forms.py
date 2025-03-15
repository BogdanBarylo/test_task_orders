from typing import List
from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields: List[str] = ["table_number"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields: List[str] = ["name", "price", "quantity"]


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    fields=["name", "price", "quantity"],
    extra=4,
    can_delete=False,
)

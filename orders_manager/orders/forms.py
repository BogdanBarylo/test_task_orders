from __future__ import annotations
from typing import Any, List, Dict
import json
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    items: forms.CharField = forms.CharField(
        widget=forms.Textarea,
        help_text=(
            "Введите список блюд в формате JSON, например: "
            '[{"name": "Салат", "price": 5.50}, '
            '{"name": "Суп", "price": 7.25}]'
        ),
    )

    class Meta:
        model = Order
        fields: List[str] = ["table_number", "items"]

    def clean_items(self) -> List[Dict[str, Any]]:
        data: str = self.cleaned_data["items"]
        try:
            items_list: Any = json.loads(data)
            if not isinstance(items_list, list):
                raise forms.ValidationError("Данные должны быть списком.")
            for item in items_list:
                if (
                    not isinstance(item, dict)
                    or "name" not in item
                    or "price" not in item
                ):
                    raise forms.ValidationError(
                        "Каждый элемент должен быть объектом с полями "
                        "'name' и 'price'."
                    )
            return items_list
        except json.JSONDecodeError:
            raise forms.ValidationError("Некорректный формат JSON.")


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields: List[str] = ["status"]

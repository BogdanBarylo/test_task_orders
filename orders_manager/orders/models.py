from __future__ import annotations
from typing import Any
from django.db import models
from django.core.validators import MinValueValidator

ORDER_STATUS_CHOICES: list[tuple[str, str]] = [
    ("pending", "В ожидании"),
    ("ready", "Готово"),
    ("paid", "Оплачено"),
]


class Order(models.Model):
    table_number: int = models.IntegerField(validators=[MinValueValidator(1)])
    items: Any = models.JSONField(
        help_text="Список заказанных блюд с ценами, например: "
        '[{"name": "Салат", "price": 5.50}, {"name": "Суп", "price": 7.25}]'
    )
    total_price: Any = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )
    status: str = models.CharField(
        max_length=10, choices=ORDER_STATUS_CHOICES, default="pending"
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Автоматический расчет общей стоимости заказа"""
        self.total_price = sum(item.get("price", 0) for item in self.items)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Заказ {self.pk} (Стол {self.table_number})"

from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from typing import List, Tuple

ORDER_STATUS_CHOICES: List[Tuple[str, str]] = [
    ("pending", "В ожидании"),
    ("ready", "Готово"),
    ("paid", "Оплачено"),
]


class Order(models.Model):
    table_number = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    status = models.CharField(
        max_length=10, choices=ORDER_STATUS_CHOICES, default="pending"
    )

    def __str__(self) -> str:
        return f"Заказ {self.pk} (Стол {self.table_number})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1,
                                           validators=[MinValueValidator(1)])

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"{self.name} (x{self.quantity})"


@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    """
    После сохранения записи OrderItem пересчитываем общую стоимость заказа.
    """
    order = instance.order
    total = sum(item.total_price for item in order.order_items.all())
    order.total_price = total
    order.save(update_fields=["total_price"])


@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    """
    После удаления записи OrderItem пересчитываем общую стоимость заказа.
    """
    order = instance.order
    total = sum(item.total_price for item in order.order_items.all())
    order.total_price = total
    order.save(update_fields=["total_price"])

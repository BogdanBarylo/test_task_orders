# Generated by Django 5.1.6 on 2025-03-12 15:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "table_number",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "items",
                    models.JSONField(
                        help_text="Список заказанных блюд с ценами,"
                        " например: "
                        "[{'name': 'Салат', 'price': 5.50}, "
                        "{'name': 'Суп', 'price': 7.25}]"
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2, editable=False, max_digits=10
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "В ожидании"),
                            ("ready", "Готово"),
                            ("paid", "Оплачено"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]

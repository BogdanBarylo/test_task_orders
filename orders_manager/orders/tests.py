from django.test import TestCase, Client
from django.urls import reverse
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm


class OrderModelTest(TestCase):
    def setUp(self) -> None:
        self.order = Order.objects.create(table_number=1, status="pending")
        OrderItem.objects.create(order=self.order, name="Салат",
                                 price=5.50, quantity=1)
        OrderItem.objects.create(order=self.order, name="Суп",
                                 price=7.25, quantity=1)

    def test_total_price_calculation(self) -> None:
        """Проверяет корректный расчет общей стоимости заказа."""
        self.order.refresh_from_db()
        expected_total = 5.50 + 7.25
        self.assertAlmostEqual(float(self.order.total_price),
                               expected_total, places=2)

    def test_order_items(self) -> None:
        """Проверяет, что заказ содержит правильные блюда
        через связь OrderItem."""
        self.order.refresh_from_db()
        items = list(self.order.order_items.values("name",
                                                   "price",
                                                   "quantity"))
        items = [
            {
                "name": item["name"],
                "price": float(item["price"]),
                "quantity": item["quantity"],
            }
            for item in items
        ]
        expected_items = [
            {"name": "Салат", "price": 5.50, "quantity": 1},
            {"name": "Суп", "price": 7.25, "quantity": 1},
        ]
        self.assertEqual(items, expected_items)


class OrderFormTest(TestCase):
    def test_order_form_valid(self) -> None:
        """Проверяет, что OrderForm корректно валидируется
        при указании номера стола."""
        form_data = {"table_number": 2}
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_order_item_form_valid(self) -> None:
        """Проверяет, что OrderItemForm валидна для корректных данных."""
        form_data = {"name": "Пицца", "price": "12.00", "quantity": 2}
        form = OrderItemForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_order_item_form_invalid(self) -> None:
        """Проверяет, что OrderItemForm не валидна при некорректных данных."""
        form_data = {"name": "Пицца", "price": "12.00", "quantity": -1}
        form = OrderItemForm(data=form_data)
        self.assertFalse(form.is_valid())


class OrderViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.order = Order.objects.create(table_number=2, status="pending")
        OrderItem.objects.create(order=self.order, name="Салат",
                                 price=5.50, quantity=1)

    def test_order_list_view(self) -> None:
        response = self.client.get(reverse("orders:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список заказов")
        self.assertContains(response, str(self.order.table_number))

    def test_order_detail_view(self) -> None:
        url = reverse("orders:detail", args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Детали заказа №{self.order.pk}")
        self.assertContains(response, str(self.order.table_number))
        self.assertContains(response, "Салат")

    def test_order_update_view(self) -> None:
        url = reverse("orders:update", args=[self.order.pk])
        data = {"status": "paid"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "paid")

    def test_order_delete_view(self) -> None:
        url = reverse("orders:delete", args=[self.order.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(pk=self.order.pk)

    def test_add_order_item_view(self) -> None:
        order = Order.objects.create(table_number=4, status="pending")
        url = reverse("orders:add_item", args=[order.pk])
        data = {"name": "Пицца", "price": "12.00", "quantity": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(order.order_items.filter(name="Пицца").exists())

    def test_revenue_view(self) -> None:
        paid_order = Order.objects.create(table_number=5, status="paid")
        OrderItem.objects.create(order=paid_order, name="Суп",
                                 price=7.25, quantity=1)
        url = reverse("orders:revenue")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(paid_order.total_price))


class OrderListFilteringTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        Order.objects.create(table_number=1, status="pending")
        Order.objects.create(table_number=2, status="paid")
        Order.objects.create(table_number=2, status="ready")

    def test_filter_by_table_number(self) -> None:
        url = reverse("orders:list")
        response = self.client.get(url, {"table_number": "2"})
        self.assertEqual(response.status_code, 200)
        orders = response.context["orders"]
        for order in orders:
            self.assertEqual(order.table_number, 2)

    def test_filter_by_status(self) -> None:
        url = reverse("orders:list")
        response = self.client.get(url, {"status": "paid"})
        self.assertEqual(response.status_code, 200)
        orders = response.context["orders"]
        for order in orders:
            self.assertEqual(order.status, "paid")

    def test_filter_by_table_and_status(self) -> None:
        url = reverse("orders:list")
        response = self.client.get(url,
                                   {"table_number": "2", "status": "ready"})
        self.assertEqual(response.status_code, 200)
        orders = response.context["orders"]
        self.assertTrue(
            all(order.table_number == 2 and
                order.status == "ready" for order in orders)
        )

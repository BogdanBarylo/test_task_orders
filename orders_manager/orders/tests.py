import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Order
from .forms import OrderForm

<<<<<<< HEAD
=======

>>>>>>> feature/ci-cd
class OrderModelTest(TestCase):
    def setUp(self) -> None:
        self.order = Order.objects.create(
            table_number=1,
<<<<<<< HEAD
            items=[{"name": "Салат", "price": 5.50}, {"name": "Суп", "price": 7.25}],
=======
            items=[{"name": "Салат", "price": 5.50},
                   {"name": "Суп", "price": 7.25}],
>>>>>>> feature/ci-cd
            status='pending'
        )

    def test_total_price_calculation(self) -> None:
        """Проверяет корректный расчет общей стоимости заказа."""
        self.order.refresh_from_db()
        expected_total = 5.50 + 7.25
<<<<<<< HEAD
        self.assertAlmostEqual(self.order.total_price, expected_total, places=2)
=======
        self.assertAlmostEqual(
            self.order.total_price, expected_total, places=2)

>>>>>>> feature/ci-cd

class OrderFormTest(TestCase):
    def test_valid_items_json(self) -> None:
        form_data = {
            "table_number": 2,
<<<<<<< HEAD
            "items": '[{"name": "Салат", "price": 5.50}, {"name": "Суп", "price": 7.25}]'
=======
            "items": '[{"name": "Салат", "price": 5.50},'
            '{"name": "Суп", "price": 7.25}]'
>>>>>>> feature/ci-cd
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_invalid_items_json(self) -> None:
        form_data = {
            "table_number": 2,
            "items": "[{'name': 'Салат', 'price': 5.50}]"
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Некорректный формат JSON", str(form.errors))

<<<<<<< HEAD
=======

>>>>>>> feature/ci-cd
class OrderViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.order = Order.objects.create(
            table_number=2,
            items=[{"name": "Салат", "price": 5.50}],
            status="pending"
        )

    def test_order_list_view(self) -> None:
        response = self.client.get(reverse('orders:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список заказов")
        self.assertContains(response, str(self.order.table_number))

    def test_order_detail_view(self) -> None:
        url = reverse('orders:detail', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Детали заказа №{self.order.pk}")
        self.assertContains(response, str(self.order.table_number))
        self.assertContains(response, "Салат")

    def test_order_create_view(self) -> None:
        url = reverse('orders:create')
        data = {
            "table_number": 3,
            "items": '[{"name": "Суп", "price": 7.25}]'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        new_order = Order.objects.get(table_number=3)
        self.assertEqual(new_order.items, [{"name": "Суп", "price": 7.25}])
        self.assertAlmostEqual(new_order.total_price, 7.25, places=2)

    def test_order_update_view(self) -> None:
        url = reverse('orders:update', args=[self.order.pk])
        data = {
            "status": "paid",
            "items": json.dumps(self.order.items)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "paid")

    def test_order_delete_view(self) -> None:
        url = reverse('orders:delete', args=[self.order.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(pk=self.order.pk)

    def test_revenue_view(self) -> None:
        paid_order = Order.objects.create(
            table_number=4,
            items=[{"name": "Суп", "price": 7.25}],
            status="paid"
        )
        url = reverse('orders:revenue')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(paid_order.total_price))

<<<<<<< HEAD
=======

>>>>>>> feature/ci-cd
class OrderListFilteringTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        Order.objects.create(
            table_number=1,
            items=[{"name": "Салат", "price": 5.50}],
            status="pending"
        )
        Order.objects.create(
            table_number=2,
            items=[{"name": "Суп", "price": 7.25}],
            status="paid"
        )
        Order.objects.create(
            table_number=2,
            items=[{"name": "Пицца", "price": 12.00}],
            status="ready"
        )

    def test_filter_by_table_number(self) -> None:
        url = reverse('orders:list')
        response = self.client.get(url, {"table_number": "2"})
        self.assertEqual(response.status_code, 200)
        orders = response.context['orders']
        for order in orders:
            self.assertEqual(order.table_number, 2)

    def test_filter_by_status(self) -> None:
        url = reverse('orders:list')
        response = self.client.get(url, {"status": "paid"})
        self.assertEqual(response.status_code, 200)
        orders = response.context['orders']
        for order in orders:
            self.assertEqual(order.status, "paid")

    def test_filter_by_table_and_status(self) -> None:
        url = reverse('orders:list')
<<<<<<< HEAD
        response = self.client.get(url, {"table_number": "2", "status": "ready"})
        self.assertEqual(response.status_code, 200)
        orders = response.context['orders']
        self.assertTrue(all(order.table_number == 2 and order.status == "ready" for order in orders))
=======
        response = self.client.get(url, {"table_number": "2",
                                         "status": "ready"})
        self.assertEqual(response.status_code, 200)
        orders = response.context['orders']
        self.assertTrue(all(
            order.table_number == 2 and order.status == "ready"
            for order in orders))
>>>>>>> feature/ci-cd

[![Cafe Manager CI/CD](https://github.com/BogdanBarylo/test_task_orders/actions/workflows/github_actions.yml/badge.svg)](https://github.com/BogdanBarylo/test_task_orders/actions/workflows/github_actions.yml)
[![codecov](https://codecov.io/github/BogdanBarylo/test_task_orders/graph/badge.svg?token=ZD3Q0UL2NL)](https://codecov.io/github/BogdanBarylo/test_task_orders)
# test_task_orders

## Описание
Данное приложение разработано на Django и предназначено для управления заказами в кафе. Система позволяет:
- Добавлять, удалять, искать и изменять заказы.
- Автоматически рассчитывать общую стоимость заказа.
- Изменять статус заказа (в ожидании, готово, оплачено).
- Отображать список заказов и детальную информацию по каждому заказу.
- Расчитывать общую выручку по заказам со статусом "оплачено".
- Предоставлять REST API для работы с заказами.

## Технологии
- Python 3.8+
- Django 4+
- Django REST Framework
- SQLite
- HTML/CSS

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <URL_репозитория>
   cd test_task_orders

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt

3. Настройка переменных окружения
В корневой директории создайте файл .env со следующим содержимым:
DJANGO_SECRET_KEY=YOUR SECRET KEY

4. Выполнение миграций базы данных
    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Запуск сервера
    ```bash
    python manage.py runserver


## REST API

Приложение предоставляет REST API для работы с заказами. Для доступа к API перейдите по адресу:

http://127.0.0.1:8000/orders/api/

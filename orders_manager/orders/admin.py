from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "table_number", "total_price", "status")
    list_filter = ("status",)
    search_fields = ("table_number",)
    inlines = [OrderItemInline]
    readonly_fields = ("total_price",)

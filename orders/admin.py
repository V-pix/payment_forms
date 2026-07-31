from decimal import Decimal

from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("item",)
    readonly_fields = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "currency",
        "status",
        "total_cost",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "currency",
        "created_at",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "city",
        "postal_code",
    )
    ordering = ("-created_at",)
    inlines = (OrderItemInline, )

    @admin.display(description="Стоимость")
    def total_cost(self, obj: OrderItem) -> Decimal | str:
        if not obj.pk:
            return "-"
        return obj.get_total_cost()

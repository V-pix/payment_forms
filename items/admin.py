from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "currency",
        "is_active",
        "created_at",
    )
    list_filter = (
        "currency",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = ("-created_at",)

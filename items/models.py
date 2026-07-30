from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.TextChoices):
    USD = "USD", _("US Dollar")
    EUR = "EUR", _("Euro")


class Item(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("Название товара"),
        help_text=_("Укажите название товара"),
    )
    description = models.TextField(
        verbose_name=_("Описание товара"),
        help_text=_("Введите описание товара"),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Цена товара"),
        help_text=_("Укажите цену товара"),
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD,
        verbose_name=_("Валюта"),
        help_text=_("Выберите валюту"),
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name=_("Активен"),
        help_text=_("Определяет, доступен ли товар для покупки"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Дата создания"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления"),
    )
    
    class Meta:
        db_table = "items"
        ordering = ("-created_at",)
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self) -> str:
        return f"{self.name} ({self.price} {self.currency})"


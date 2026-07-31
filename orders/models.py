from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from items.models import Item


class OrderStatus(models.TextChoices):
    CREATED = "created", _("Создан")
    PAID = "paid", _("Оплачен")
    FAILED = "failed", _("Ошибка оплаты")
    CANCELED = "canceled", _("Отменен")


class Order(models.Model):
    first_name = models.CharField(
        max_length=50,
        verbose_name=_("Имя"),
        help_text=_("Введите имя покупателя"),
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name=_("Фамилия"),
        help_text=_("Введите фамилию покупателя"),
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        help_text=_("Введите email"),
    )
    address = models.CharField(
        max_length=250,
        verbose_name=_("Адрес"),
        help_text=_("Введите адрес доставки"),
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name=_("Почтовый индекс"),
        help_text=_("Введите почтовый индекс"),
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("Город"),
        help_text=_("Введите город"),
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
        db_index=True,
        verbose_name=_("Статус"),
    )
    currency = models.CharField(
        max_length=3,
        default="USD",
        verbose_name=_("Валюта"),
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
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self) -> str:
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Item,
        related_name="order_items",
        on_delete=models.PROTECT
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    
    class Meta:
        verbose_name = _("Позиция заказа")
        verbose_name_plural = _("Позиции заказа")

    def __str__(self) -> str:
        return f"{self.id}, {self.order.id}, {self.item.name}, {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs) -> None:
        if self.item_id:
            if self.price is None:
                self.price = self.item.price
        return super().save(*args, **kwargs)

from decimal import Decimal
from typing import Iterator

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpRequest

from items.models import Item


class Cart:
    def __init__(self, request: HttpRequest):
        self.session = request.session
        self.data = self.session.get(settings.CART_SESSION_ID, {})

    def __iter__(self) -> Iterator[dict]:
        items = Item.objects.filter(id__in=self.data.keys(), is_active=True)
        cart_data = self.data.copy()
        for item in items:
            line = cart_data[str(item.id)].copy()
            line["item"] = item
            line["price"] = Decimal(line["price"])
            line["total"] = line["price"] * line["quantity"]
            yield line

    def __len__(self) -> int:
        return sum(line["quantity"] for line in self.data.values())

    @property
    def currency(self) -> str:
        currencies = {line["currency"] for line in self.data.values()}
        if not currencies:
            return ""
        if len(currencies) != 1:
            raise ValidationError("Корзина содержит товары в разных валютах")
        return next(iter(currencies))

    def add(
        self,
        item: Item,
        quantity: int = 1,
        override: bool = False
    ) -> None:
        if self.data and self.currency != item.currency:
            raise ValidationError(
                "В одном заказе могут быть товары только в одной валюте"
            )
        item_id = str(item.id)
        if item_id not in self.data:
            self.data[item_id] = {
                "quantity": 0,
                "price": str(item.price),
                "currency": item.currency,
            }
        self.data[item_id]["quantity"] = (
            quantity if override else self.data[item_id]["quantity"] + quantity
        )
        self.save()

    def remove(self, item: Item) -> None:
        item_id = str(item.id)
        if item_id in self.data:
            self.data.pop(item_id)
            self.save()

    def get_total_price(self) -> Decimal:
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.data.values()
        )

    def clear(self) -> None:
        self.session.pop(settings.CART_SESSION_ID, None)
        self.session.modified = True
        self.data = {}

    def save(self) -> None:
        self.session[settings.CART_SESSION_ID] = self.data
        self.session.modified = True

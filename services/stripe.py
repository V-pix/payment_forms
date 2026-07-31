from decimal import Decimal

import stripe
from django.conf import settings

from items.models import Item
from orders.models import Order


def create_item_checkout_session(
    *,
    item: Item,
    success_url: str,
    cancel_url: str,
) -> stripe.checkout.Session:
    return stripe.checkout.Session.create(
        api_key=settings.STRIPE_SECRET_KEY,
        mode="payment",
        payment_method_types=["card"],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "item_id": str(item.id),
        },
        line_items=[
            {
                "price_data": {
                    "currency": item.currency.lower(),
                    "product_data": {
                        "name": item.name,
                        "description": item.description[:500],
                    },
                    "unit_amount": int(item.price * Decimal("100")),
                },
                "quantity": 1,
            }
        ],
    )


def create_order_checkout_session(
    *,
    order: Order,
    success_url: str,
    cancel_url: str,
) -> stripe.checkout.Session:
    line_items = [
        {
            "price_data": {
                "currency": order.currency.lower(),
                "product_data": {
                    "name": order_item.item.name,
                },
                "unit_amount": int(order_item.price * Decimal("100")),
            },
            "quantity": order_item.quantity,
        }
        for order_item in order.items.all()
    ]

    return stripe.checkout.Session.create(
        api_key=settings.STRIPE_SECRET_KEY,
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=order.email,
        line_items=line_items,
    )

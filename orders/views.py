import os
from decimal import Decimal
import stripe

from django.db import transaction
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from cart.cart import Cart
from services.stripe import create_order_checkout_session
from .forms import OrderCreateForm
from .models import Order, OrderItem, OrderStatus


@require_http_methods(["GET", "POST"])
def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if not cart:
        messages.info(request, "Корзина пуста")
        return redirect("items:list")
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.currency = cart.currency
                order.save()
                OrderItem.objects.bulk_create(
                    [
                        OrderItem(
                            order=order,
                            item=cart_line["item"],
                            price=cart_line["price"],
                            quantity=cart_line["quantity"],
                        )
                        for cart_line in cart
                    ]
                )
            cart.clear()
            request.session["order_id"] = order.id
            return redirect("orders:process")
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html", {"cart": cart, "form": form})


@require_http_methods(["GET", "POST"])
def payment_process(request: HttpRequest) -> HttpResponse:
    order_id = request.session.get("order_id")
    if not order_id:
        return redirect("cart:cart_detail")
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        try:
            session = create_order_checkout_session(
                order=order,
                success_url=request.build_absolute_uri(reverse("orders:completed")),
                cancel_url=request.build_absolute_uri(reverse("orders:canceled")),
            )
        except stripe.StripeError:
            messages.error(request, "Не удалось создать платёжную сессию")
        else:
            return redirect(session.url, code=303)

    return render(request, "orders/process.html", {"order": order})


def payment_completed(request: HttpRequest) -> HttpResponse:
    order = Order.objects.filter(pk=request.session.get("order_id")).first()
    return render(request, "orders/completed.html", {"order": order})


def payment_canceled(request: HttpRequest) -> HttpResponse:
    order = Order.objects.filter(pk=request.session.get("order_id")).first()
    if order and order.status == OrderStatus.CREATED:
        order.status = OrderStatus.CANCELED
        order.save(update_fields=["status", "updated_at"])
    return render(request, "orders/canceled.html", {"order": order})

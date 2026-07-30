import os

import stripe
from cart.forms import CartAddProductForm, CartAddItemForm
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from dotenv import find_dotenv, load_dotenv

from .models import Item

load_dotenv(find_dotenv())
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@csrf_exempt
def create_checkout_session(request, pk: int):
    if request.method == "GET":
        domain_url = os.getenv("DOMAIN_URL")
        item = Item.objects.get(id=pk)
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=(domain_url
                             + "success?session_id={CHECKOUT_SESSION_ID}"),
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                metadata={"item_id": item.id},
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": item.name,
                            },
                            "unit_amount": 300,
                        },
                        "quantity": 1,
                    },
                ],
            )
            return JsonResponse({"id": checkout_session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class BuyItemView(TemplateView):
    template_name = "items/item.html"

    def get_context_data(self, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=item_id)
        context = super(BuyItemView, self).get_context_data(**kwargs)
        context.update(
            {
                "item": item,
                "STRIPE_PUBLIC_KEY": os.getenv("STRIPE_PUBLIC_KEY"),
            }
        )
        return context


class SuccessView(TemplateView):
    template_name = "items/success.html"


class CancelView(TemplateView):
    template_name = "items/cancel.html"


@require_GET
def item_list(request: HttpRequest):
    # items = Item.objects.filter(is_active=True)
    items = Item.objects.all()
    return render(request, "items/item_list.html", {"items": items})


@require_GET
def item_detail(request: HttpRequest, pk: int):
    item = get_object_or_404(Item, pk=pk, is_active=True)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "items/item_detail.html",
        {
            "item": item,
            # "stripe_public_key": StripeCheckoutService.get_public_key(item.currency),
            # "cart_form": CartAddProductForm(),
            "cart_product_form": cart_product_form
        },
    )


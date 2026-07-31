import stripe
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic.base import TemplateView

from cart.forms import CartAddProductForm
from services.stripe import create_item_checkout_session

from .models import Item


@require_GET
def create_checkout_session(request: HttpRequest, pk: int) -> JsonResponse:
    item = get_object_or_404(Item, pk=pk, is_active=True)
    try:
        checkout_session = create_item_checkout_session(
            item=item,
            success_url=(
                request.build_absolute_uri(reverse("items:success"))
                + "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=request.build_absolute_uri(reverse("items:cancel")),
        )
    except stripe.StripeError as error:
        return JsonResponse({"error": str(error)}, status=400)
    return JsonResponse({"id": checkout_session.id})


class BuyItemView(TemplateView):
    template_name = "items/item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = get_object_or_404(
            Item,
            pk=self.kwargs["pk"],
            is_active=True,
        )
        context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
        return context


class SuccessView(TemplateView):
    template_name = "items/success.html"


class CancelView(TemplateView):
    template_name = "items/cancel.html"


@require_GET
def item_list(request: HttpRequest):
    items = Item.objects.filter(is_active=True)
    return render(request, "items/item_list.html", {"items": items})


@require_GET
def item_detail(request: HttpRequest, pk: int):
    item = get_object_or_404(Item, pk=pk, is_active=True)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        "items/item_detail.html",
        {"item": item, "cart_product_form": cart_product_form},
    )

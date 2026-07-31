from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from items.models import Item

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request: HttpRequest, item_id: int) -> HttpResponse:
    cart = Cart(request)
    item = get_object_or_404(Item, pk=item_id, is_active=True)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        try:
            cart.add(
                item=item,
                quantity=form.cleaned_data["quantity"],
                override=form.cleaned_data["override"],
            )
        except ValidationError as exc:
            messages.error(request, exc.message)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(Item, pk=item_id)
    Cart(request).remove(item)
    return redirect("cart:cart_detail")


def cart_detail(request: HttpRequest) -> HttpResponse:
    return render(request, "cart/cart_detail.html", {"cart": Cart(request)})

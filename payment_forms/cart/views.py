from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from items.models import Item

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, item_id: int):
    cart = Cart(request)
    item = get_object_or_404(Item, pk=item_id, is_active=True)
    form = CartAddProductForm(request.POST)
    print("Добавление товара в корзину")
    print("item_id=%s", item_id)
    print("POST=%s", request.POST)
    print("cart.data до добавления=%s", cart.data)
    print("session до добавления=%s", dict(request.session))
    if form.is_valid():
        try:
            cart.add(
                item=item,
                quantity=form.cleaned_data["quantity"],
                override=form.cleaned_data["override"]
            )
        except ValidationError as exc:
            messages.error(request, exc.message)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, item_id: int):
    item = get_object_or_404(Item, pk=item_id)
    Cart(request).remove(item)
    return redirect("cart:detail")


def cart_detail(request):
    return render(request, "cart/cart_detail.html", {"cart": Cart(request)})

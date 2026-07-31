from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("items.urls")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("admin/", admin.site.urls),
]

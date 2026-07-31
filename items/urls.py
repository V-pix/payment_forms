from django.urls import path

from . import views
from .views import BuyItemView, CancelView, SuccessView

app_name = "items"

urlpatterns = [
    path("buy/<int:pk>/", views.create_checkout_session, name="buy"),
    path("item/<int:pk>/", BuyItemView.as_view(), name="buy_item"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("success/", SuccessView.as_view(), name="success"),
    path("", views.item_list, name="item_list"),
    path("item/detail/<int:pk>/", views.item_detail, name="item_detail"),
]

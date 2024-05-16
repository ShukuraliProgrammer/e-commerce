from django.urls import path
from .views import AddToCartView, UpdateUserCartItem

urlpatterns = [
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart-items/<int:product_id>/", UpdateUserCartItem.as_view(), name="update-cart-item")
]

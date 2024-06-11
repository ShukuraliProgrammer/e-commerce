from django.urls import path
from .views import AddToCartView, UpdateUserCartItem, DeleteUserCartItemView, CartItemsListView, OrderCreateView

urlpatterns = [
    path("", OrderCreateView.as_view(), name="order-create"),
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart-items/", CartItemsListView.as_view(), name="cart-items-list"),
    path("cart-items/<int:product_id>/", UpdateUserCartItem.as_view(), name="update-cart-item"),
    path("cart-items/<int:id>/delete", DeleteUserCartItemView.as_view(), name="delete-cart-item"),

]

from django.urls import path
from .views import AddToCartView, UpdateUserCartItem, DeleteUserCartItemView, CartItemsListView, OrderCreateView, \
    OrderListAPIView, OrderDetailAPIView, OrderCancelAPIView, OrderDiscountAPIView

urlpatterns = [
    path("", OrderListAPIView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("create", OrderCreateView.as_view(), name="order-create"),
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart-items/", CartItemsListView.as_view(), name="cart-items-list"),
    path("cart-items/<int:product_id>/", UpdateUserCartItem.as_view(), name="update-cart-item"),
    path("cart-items/<int:id>/delete", DeleteUserCartItemView.as_view(), name="delete-cart-item"),
    path("order-cancel/<int:pk>/", OrderCancelAPIView.as_view(), name="order-cancel"),
    path("order-discount/", OrderDiscountAPIView.as_view(), name="order-discount")
]

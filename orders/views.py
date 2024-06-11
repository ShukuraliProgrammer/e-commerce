from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView, CreateAPIView
from .serialziers import AddToCartSerializer, UpdateCartItemSerializer, CartItemListSerializer, OrderCreateSerializer
from .models import CartItem, Order
from django.shortcuts import get_object_or_404
from products.models import Product
from accounts.models import UserAddress

class AddToCartView(APIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(data={"message": "invalid_data"}, status=status.HTTP_400_BAD_REQUEST)
            data = serializer.validated_data
            product = Product.objects.get(id=data.get("product_id"))
            item = CartItem.objects.create(user=request.user, quantity=data.get("quantity"), product=product)

            return Response(data={"message": "cart_item_added", "result": {"cart_item_id": item.id}})
        except Product.DoesNotExist:
            return Response(data={"message": "product_not_found"}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserCartItem(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = UpdateCartItemSerializer
    lookup_field = 'product_id'
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart_item = self.queryset.get(user=self.request.user, product_id=self.kwargs.get(self.lookup_field))
        return cart_item


class DeleteUserCartItemView(DestroyAPIView):
    queryset = CartItem.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCartItemSerializer


class CartItemsListView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(data={"message": "invalid_data"}, status=status.HTTP_400_BAD_REQUEST)
            address = UserAddress.objects.get(id=serializer.validated_data.get("user_address"))
            cart_items = CartItem.objects.filter(id__in=serializer.validated_data.get("cart_items"))
            total_price = sum([item.product.price for item in cart_items])
            order = Order.objects.create(user=request.user, address=address, total_price=total_price)
            return Response(data={"message": "order_created", "result": {"order_id": order.id}})

        except Exception as e:
            return Response(data={"message": "error", "result": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
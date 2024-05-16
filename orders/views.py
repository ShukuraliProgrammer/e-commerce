from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from .serialziers import AddToCartSerializer, UpdateCartItemSerializer
from .models import CartItem
from django.shortcuts import get_object_or_404
from products.models import Product


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

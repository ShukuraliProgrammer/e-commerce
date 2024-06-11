from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductListSerializer


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("quantity",)


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = CartItem
        exclude = ('user',)



class OrderCreateSerializer(serializers.Serializer):
    cart_items = serializers.ListField(child=serializers.IntegerField())
    user_address = serializers.IntegerField(required=True)
    subtotal_price = serializers.FloatField(required=True)




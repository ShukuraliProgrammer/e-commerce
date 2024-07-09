from rest_framework import serializers
from .models import CartItem, Order, DeliveryTariff, Discount
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


class OrderListSerializer(serializers.ModelSerializer):
    items = CartItemListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'items', 'total_price']


class DeliveryTariffSerializer(serializers.ModelSerializer):
    regions = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryTariff
        fields = ("branch", "high", "width", "weight", "price", "regions", "delivery_time")

    def get_regions(self, obj):
        return obj.regions.values_list('name', flat=True)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("code", "max_limit_price")


class OrderDetailSerializer(serializers.ModelSerializer):
    items = CartItemListSerializer(many=True)
    delivery_tariff = DeliveryTariffSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = Order
        fields = ['id', 'status', 'items', 'total_price', 'address', 'discount', 'payment_status', 'payment_method',
                  'delivery_tariff']


class OrderDiscountSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    discount_code = serializers.CharField(required=True)


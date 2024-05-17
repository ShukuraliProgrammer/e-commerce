from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from products.models import Category, Product, ProductColour, ProductSize, ProductReview
from products.seralizers import CategoryListSerializer, ProductListSerializer, ProductColourListSerializer, \
    ProductSizeListSerializer, ProductReviewListSerializer

from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = None


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', "colours", "sizes"]

    def get_queryset(self):
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        if min_price and max_price:
            queryset = self.queryset.filter(price__gte=min_price, price__lte=max_price)
        elif min_price is None and max_price:
            queryset = self.queryset.filter(price__lte=max_price)

        elif max_price is None and min_price:
            queryset = self.queryset.filter(price__gte=min_price)
        else:
            queryset = self.queryset.all()
        return queryset


class ProductColourListView(ListAPIView):
    queryset = ProductColour.objects.all()
    serializer_class = ProductColourListSerializer


class ProductSizeListView(ListAPIView):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeListSerializer


class ProductReviewsListView(ListAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewListSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id is None:
            return self.queryset.filter(product_id=product_id)
        return Response(
            data={
                'status': false,
                'messeage': 'No reviews'
            }
        )
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from products.models import Category, Product, ProductColour, ProductSize, ProductReview
from products.serializers import CategoryListSerializer, ProductListSerializer, ProductColourListSerializer, \
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
        if product_id is not None:
            return self.queryset.filter(product_id=product_id)
        data = {
            'status': False,
            'messeage': 'No reviews'
        }
        return Response(data=data)


class RelatedProductsView(APIView):
    http_method_names = ['get', ]
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            products = Product.objects.filter(category=product.category)
            serializer = ProductListSerializer(products, many=True).data
            return Response(serializer)

        except Product.DoesNotExist:
            data = {
                'status': False,
                'message': 'Product does not found'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            raise e

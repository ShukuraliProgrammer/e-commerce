from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView

from products.models import Category, Product, ProductColour, ProductReview, ProductSize
from products.seralizers import CategoryListSerializer, ProductListSerializer, ProductColourListSerializer, ProductReviewSerializer, \
    ProductSizeListSerializer

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response

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


class ProductReviewListView(APIView):

    def get(self, request):
        book = ProductReview.objects.all()
        serializer = ProductReviewSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post (self, request):
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewDetailApiView(APIView):
    def get(self, request, product_id):
        try:
            get_object_or_404(ProductReview, id=product_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=product_id)
        serializer = ProductReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def puch(self, request, product_id):
        try:
            get_object_or_404(ProductReview, id=product_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=product_id)
        serializer = ProductReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,product_id ):
        try:
            get_object_or_404(ProductReview, id=product_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=product_id)
        review.delete()
        data = {
            "message": "O'chirildi"
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)





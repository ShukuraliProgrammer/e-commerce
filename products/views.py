from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from products.models import Category, Product, ProductColour, ProductSize, ProductReview
from products.serializers import CategoryListSerializer, ProductListSerializer, ProductColourListSerializer, \
    ProductSizeListSerializer, AddReviewToProductSerializer, ProductReviewUpdateSerializer
from django.core.exceptions import ObjectDoesNotExist
from products.models import Category, Product, ProductColour, ProductReview, ProductSize
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


class AddReviewToProductApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddReviewToProductSerializer

    def post(self, request):
        try:
            serializer = AddReviewToProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            serializer.save(user=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            data = {
                "detail": str(e.detail)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductReviewDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductReviewUpdateSerializer

    def patch(self, request, review_id):
        try:
            get_object_or_404(ProductReview, id=review_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=review_id)
        serializer = AddReviewToProductSerializer(instance=review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, review_id):
        try:
            get_object_or_404(ProductReview, id=review_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=review_id)
        serializer = self.serializer_class(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        try:
            get_object_or_404(ProductReview, id=review_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=review_id)
        review.delete()
        data = {
            "message": "O'chirildi"
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class RelatedProductsView(APIView):
    http_method_names = ['get', ]

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            products = Product.objects.filter(category=product.category).exclude(id=id)
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

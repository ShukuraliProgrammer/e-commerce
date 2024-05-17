from django.urls import path

from products.views import *

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("colours/", ProductColourListView.as_view(), name="colours"),
    path("sizes/", ProductSizeListView.as_view(), name="sizes"),
    path("reviews/", ProductReviewsListView.as_view(), name="reviews")
]

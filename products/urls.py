from django.urls import path

from products.views import *

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("products/", ProductListAPIView.as_view(), name="products"),
]

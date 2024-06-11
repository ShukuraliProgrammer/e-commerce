from django.urls import path

from products.views import *

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path("products/", ProductListAPIView.as_view(), name="products"),
    path("colours/", ProductColourListView.as_view(), name="colours"),
    path("sizes/", ProductSizeListView.as_view(), name="sizes"),
    path("review/", AddReviewToProductApiView.as_view(), name="review"),
    path("review/<int:review_id>", ProductReviewDetailApiView.as_view(), name="detail-review"),
    path("related-products/<int:id>", RelatedProductsView.as_view(), name="related-products"),

]

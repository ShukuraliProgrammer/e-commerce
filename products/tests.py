from django.urls import reverse
from accounts.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import ProductReview, Product, Category
from products.serializers import ProductReviewListSerializer


class ProductReviewsListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser@gmail.com', password='1234')
        self.category = Category.objects.create(name='AAAA')
        self.product = Product.objects.create(
            name='category',
            price=2.03,
            short_description='short_description',
            description='description',
            quanttity=1,
            instructions='text',
            category=self.category,
            in_stock=True,
            brand='brand',
            discount=5
        )
        self.product_review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            title='title',
            email='testemail@gmal.com',
            rank=5,
            review="Great product"
        )

    def test_get_reviews_by_product_id(self):
        url = reverse('reviews')
        response = self.client.get(url, {'product_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProductReviewListSerializer(ProductReview.objects.filter(product_id=1), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_reviews_no_product_id(self):
        url = reverse('reviews')
        response = self.client.get(url, {'product_id': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

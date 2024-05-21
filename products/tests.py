from rest_framework.test import APITestCase
from django.urls import reverse

from products.models import Product, ProductReview
from accounts.models import User


class ReviewAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@gmail.com', password='0204')
        cls.product = Product.objects.create(
            name='sddc',
            price=2.03,
            short_description='ffj',
            description='ooo',
            quanttity=1,
            instructions='poo',

        )

    def test_get_all_review_of_product(self):

        response = ProductReview.objects.create(
            product=1,
            user=self.user,
            title='title',
            review='review',
            rank=1,
            email='test@gamil.com'
        )
        self.assertEqual(response.product, 1)


from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from common.models import Media
from products.models import Product, Category


class TestAddProductReview(APITestCase):
    def setUp(self):
       url = reverse("register")
       data = {
            "first_name": "TestName",
            "last_name": "TestLastName",
            "email": "testemail@gmail.com",
            "password": "test12345_"
        }
       response = self.client.post(url, data=data)
       catigory = Category.objects.create(name='name')
       user = User.objects.get(id=1)
       user.is_active = True
       user.save()
       Media.objects.create(type="IMAGE")
       Product.objects.create(
            name='aa',
            price=12,
            short_description='hello',
            description='hello',
            quanttity=12,
            instructions='1231',
            in_stock=True,
            brand='coco',
            discount=0,
            category_id=1,
            thumbnail_id=1
        )

    def test_add_review(self):
        payload = {"email": "testemail@gmail.com", "password": "test12345_"}
        login_url = reverse('login')
        response = self.client.post(login_url, data=payload)
        token = response.json()['access']
        header = {"Authorization": f"Bearer {token}"}
        review = {
            "product_id": 1,
            "title": "salom",
            "review": "sinov chun",
            "rank": 5,
            "email": "unirxojiddin@gmai.com"
        }
        response = self.client.post("http://127.0.0.1:8000/products/review/", data=review, headers=header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['title', 'review', 'rank', 'email'])
        self.assertEqual(response.data['title'], "salom")
        self.assertEqual(response.data['review'], "sinov chun")
        self.assertEqual(response.data['rank'], 5)
        self.assertEqual(response.data['email'], "unirxojiddin@gmai.com")

    def test_get_review(self):
        payload = {"email": "testemail@gmail.com", "password": "test12345_"}
        login_url = reverse('login')
        response = self.client.post(login_url, data=payload)
        token = response.json()['access']
        header = {"Authorization": f"Bearer {token}"}
        review = {
            "product_id": 1,
            "title": "salom",
            "review": "sinov chun",
            "rank": 5,
            "email": "unirxojiddin@gmai.com"
        }
        self.client.post("http://127.0.0.1:8000/products/review/", data=review, headers=header)
        response = self.client.get("http://127.0.0.1:8000/products/review/1", headers=header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['title', 'review', 'rank', 'email'])
        self.assertEqual(response.data['title'], "salom")
        self.assertEqual(response.data['review'], "sinov chun")
        self.assertEqual(response.data['rank'], 5)
        self.assertEqual(response.data['email'], "unirxojiddin@gmai.com")

    def test_put_review(self):
        payload = {"email": "testemail@gmail.com", "password": "test12345_"}
        login_url = reverse('login')
        response = self.client.post(login_url, data=payload)
        token = response.json()['access']
        header = {"Authorization": f"Bearer {token}"}
        review = {
            "product_id": 1,
            "title": "salom",
            "review": "sinov chun",
            "rank": 5,
            "email": "unirxojiddin@gmai.com"
        }
        self.client.post("http://127.0.0.1:8000/products/review/", data=review, headers=header)
        put_review = {
            "product_id":1,
            "title": "Assalom",
            "review": "sinov chun",
            "rank": 4,
            "email": "umirxojiddin@gmai.com"
        }
        response = self.client.put("http://127.0.0.1:8000/products/review/1",  data=put_review, headers=header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['title', 'review', 'rank', 'email'])
        self.assertEqual(response.data['title'], "Assalom")
        self.assertEqual(response.data['review'], "sinov chun")
        self.assertEqual(response.data['rank'], 4)
        self.assertEqual(response.data['email'], "umirxojiddin@gmai.com")

    def test_patch_review(self):
        payload = {"email": "testemail@gmail.com", "password": "test12345_"}
        login_url = reverse('login')
        response = self.client.post(login_url, data=payload)
        token = response.json()['access']
        header = {"Authorization": f"Bearer {token}"}
        review = {
            "product_id": 1,
            "title": "salom",
            "review": "sinov chun",
            "rank": 5,
            "email": "unirxojiddin@gmai.com"
        }
        self.client.post("http://127.0.0.1:8000/products/review/", data=review, headers=header)
        patch_review = {
            "title": "Assalom",
            "review": "ana yana"

        }
        response = self.client.patch("http://127.0.0.1:8000/products/review/1",  data=patch_review, headers=header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.data.keys()), ['title', 'review', 'rank', 'email'])
        self.assertEqual(response.data['title'], "Assalom")
        self.assertEqual(response.data['review'], "ana yana")

    def test_delete_review(self):
        payload = {"email": "testemail@gmail.com", "password": "test12345_"}
        login_url = reverse('login')
        response = self.client.post(login_url, data=payload)
        token = response.json()['access']
        header = {"Authorization": f"Bearer {token}"}
        review = {
            "product_id": 1,
            "title": "salom",
            "review": "sinov chun",
            "rank": 5,
            "email": "unirxojiddin@gmai.com"
        }
        self.client.post("http://127.0.0.1:8000/products/review/", data=review, headers=header)
        response = self.client.delete("http://127.0.0.1:8000/products/review/1", headers=header)
        self.assertEqual(response.status_code, 204)
        response = self.client.get("http://127.0.0.1:8000/products/review/1", headers=header)
        self.assertEqual(response.status_code, 404)

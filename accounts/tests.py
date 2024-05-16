from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User

class TestUserCreateView(APITestCase):
    def setUp(self):
        pass

    def test_happy(self):
        url = reverse("register")
        data = {
            "first_name": "TestName",
            "last_name": "TestLastName",
            "email": "testemail@gmail.com",
            "password": "test12345_"
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(list(response.data.keys()), ['first_name', 'last_name', 'email', 'password'])
        self.assertEqual(response.data["first_name"], "TestName")



class TestVerifyOtpView(APITestCase):
    def setUp(self):
        self.new_user = User.objects.create(email="testemail@gmail.com", last_name="TestLastName", first_name="TestName")
        self.new_user.set_password("test12345_")
        self.new_user.save()

    def test_happy(self):
        pass

    def test_with_invalid_otp(self):
        pass

    def test_with_activated_otp_code(self):
        pass



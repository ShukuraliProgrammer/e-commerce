from django.urls import path

from accounts.views import *

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
]

from django.shortcuts import render

from rest_framework.generics import CreateAPIView

from accounts.models import *
from accounts.serializers import *


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer



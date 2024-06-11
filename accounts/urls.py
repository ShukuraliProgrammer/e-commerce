from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.views import *

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/start/', ResetPasswordStartView.as_view(), name='reset_password_start'),
    path('reset-password/finish/', ResetPasswordFinishView.as_view(), name='reset_password_finish'),
    path("address/", UserAddressCreateView.as_view(), name="address"),
    path("address/<int:id>/", UserAddressUpdateView.as_view(), name="address_update"),
]

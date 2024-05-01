from rest_framework import serializers
from django.utils import timezone
from django.conf import settings
from accounts.models import User, VerifictionOtp
from accounts.utils import generate_code, send_email


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data.get("email"), is_active=False)
        if user.exists():
            sms = VerifictionOtp.objects.get(user=user, type=VerifictionOtp.VerificationType.REGISTER,
                                             expires_in__lt=timezone.now(), is_active=True)
            if sms:
                sms.expires_in = timezone.now() + settings.OTP_CODE_ACTIVATION_TIME
                code = generate_code()
                sms.code = code
                send_email(code=code, email=user.email)

        return self.create(self, validated_data)


class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)
    verify_type = serializers.ChoiceField(choices=VerifictionOtp.VerificationType)


class ResetPasswordStartSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordFinishSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('Passwords do not match')

        return attrs

import secrets
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from core.settings.base import EMAIL_HOST
def check_otp_code(value):
    if len(str(value)) != 6:
        raise ValidationError("Otp code must be 6 digits")


def send_email(code, email):
    message = f"Your OTP code is: {code}"
    send_mail(subject="Registration OTP Code", message=message, from_email=EMAIL_HOST, recipient_list=[email], fail_silently=False)


def generate_code():
    numbers = '123456789'
    return "".join(secrets.choice(numbers) for i in range(6))

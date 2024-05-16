from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_code_to_email(code, email):
    message = f"Your OTP code is: {code}"
    send_mail(subject="Registration OTP Code", message=message, from_email=settings.EMAIL_HOST, recipient_list=[email],
              fail_silently=False)

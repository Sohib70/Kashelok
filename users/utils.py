import random
import string
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta

def generate_code():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=6))

def send_to_mail(email, code):
    subject = "Tasdiqlash kodi"
    message = f"Sizning kodingiz: {code}"
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
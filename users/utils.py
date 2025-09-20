import random
import string
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

def generate_code():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=6))

def send_to_mail(email, code):
    subject = _("Tasdiqlash kodi")
    message = _("Sizning kodingiz: %(code)s") % {"code": code}
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )

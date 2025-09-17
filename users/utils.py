import random
import string

from django.core.mail import send_mail

def generate_code():
    letter = string.ascii_letters + string.digits
    return ''.join([letter[random.randint(0,len(letter))] for _ in range(6)])

def send_to_mail(email, code):
    subject = "Tasdiqlash kodi"
    message = f"Sizning kodingiz {code}"
    send_mail(subject=subject,message=message,from_email=None,recipient_list=[email, ])
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.username
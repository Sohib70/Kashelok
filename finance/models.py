from django.db import models
from django.conf import settings
from django.utils import timezone

class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="income_images/", blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="expense_images/", blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.amount}"

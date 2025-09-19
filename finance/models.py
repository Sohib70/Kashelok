from django.db import models
from django.conf import settings
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(
        upload_to="income_images/",
        blank=True,
        null=True,
        default="income_images/default.jpg"
    )

    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(
        upload_to="expense_images/",
        blank=True,
        null=True,
        default="expense_images/default.jpg"
    )

    def __str__(self):
        return self.name


class Income(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('dollar', 'Dollar'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(default=datetime.today)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.amount}"


class Expense(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('dollar', 'Dollar'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(default=datetime.today)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.amount}"


class UserBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    card = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dollar = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def total_balance(self, dollar_to_sum=12300):
        return self.cash + self.card + (self.dollar * dollar_to_sum)

    def __str__(self):
        return f"{self.user.username} Balans"

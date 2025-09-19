from django.db import models
from django.conf import settings
from datetime import date

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.product_name} - {self.amount}"

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.product_name} - {self.amount}"

from django.contrib import admin
from .models import Category,Income,ExpenseCategory
# Register your models here.
admin.site.register(Category)
admin.site.register(ExpenseCategory)
admin.site.register(Income)
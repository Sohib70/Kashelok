from django import forms
from .models import Income,Category,Expense,ExpenseCategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image"]

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name", "image"]

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["amount", "comment", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["amount", "comment", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }
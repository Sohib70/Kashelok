from django import forms
from .models import Income, Category, Expense, ExpenseCategory, UserBalance
from django.utils.translation import gettext_lazy as _

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }

PAYMENT_CHOICES = (
    ('cash', _('Naqd')),
    ('card', _('Karta')),
    ('dollar', _('Dollar')),
)

class IncomeForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Income
        fields = ["amount", "comment", "date", "payment_method"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

class ExpenseForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Expense
        fields = ["amount", "comment", "date", "payment_method"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

class UserBalanceForm(forms.ModelForm):
    class Meta:
        model = UserBalance
        fields = ["cash", "card", "dollar"]
        widgets = {
            "cash": forms.NumberInput(attrs={"class": "form-control"}),
            "card": forms.NumberInput(attrs={"class": "form-control"}),
            "dollar": forms.NumberInput(attrs={"class": "form-control"}),
        }

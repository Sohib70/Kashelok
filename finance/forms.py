from django import forms
from .models import Income, Expense

class DateInput(forms.DateInput):
    input_type = "date"

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["title", "image", "description", "amount", "date"]
        widgets = {
            "date": DateInput(),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "image", "description", "amount", "date"]
        widgets = {
            "date": DateInput(),
        }

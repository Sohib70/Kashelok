from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Parol")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Parolni tasdiqlang")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'image']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos emas")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username / Email / Telefon")
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")

class ResetPasswordForm(forms.Form):
    code = forms.CharField(max_length=6, label="Kod")
    new_pass = forms.CharField(widget=forms.PasswordInput, label="Yangi parol")
    confirm_pass = forms.CharField(widget=forms.PasswordInput, label="Parolni tasdiqlash")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name","image"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Eski parol")
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Yangi parol")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Yangi parolni tasdiqlash")


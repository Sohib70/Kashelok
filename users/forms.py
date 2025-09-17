from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

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


class ChangePassForm(forms.Form):
    old_pass = forms.CharField(label="Eski parol", widget=forms.PasswordInput)
    new_pass = forms.CharField(label="Yangi parol", widget=forms.PasswordInput)
    confirm_pass = forms.CharField(label="Parolni tasdiqlang", widget=forms.PasswordInput)
    code = forms.CharField(label="Tasdiqlash kodi", max_length=6)



class ResetPassForm(forms.Form):
    password = forms.CharField(
        label="Yangi parol",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Yangi parolingizni kiriting"
        })
    )
    password_confirm = forms.CharField(
        label="Parolni tasdiqlang",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Parolni qayta kiriting"
        })
    )
    code = forms.CharField(
        label="Tasdiqlash kodi",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "SMS kodni kiriting"
        })
    )
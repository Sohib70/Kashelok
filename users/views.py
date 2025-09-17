from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import datetime, timedelta
from .forms import ForgotPasswordForm, ResetPasswordForm
from .utils import generate_code, send_to_mail
from .models import CustomUser
from .forms import ProfileForm,CustomPasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Ro‘yxatdan o‘tish muvaffaqiyatli! Endi login qiling.")
            return redirect("login")
        else:
            messages.error(request, "❌ Ma’lumotlar noto‘g‘ri. Qayta tekshiring.")
    else:
        form = SignUpForm()
    return render(request, "accound/signup.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "accound/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def profile_view(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)

    if request.method == "POST":
        if "save_profile" in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "✅ Profil muvaffaqiyatli yangilandi!")
                return redirect("profile")

        elif "change_password" in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "🔑 Parol muvaffaqiyatli o‘zgartirildi!")
                return redirect("profile")

    return render(request, "accound/profile.html", {
        "form": profile_form,
        "password_form": password_form,
    })


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "❌ Bunday foydalanuvchi topilmadi!")
                return redirect("forgot_password")

            code = generate_code()
            request.session["pass_code"] = code
            request.session["reset_username"] = username
            request.session["code_created"] = datetime.now().timestamp()

            send_to_mail(user.email, code)
            print(f"Kod konsolga: {code}")

            messages.success(request, "✅ Kod foydalanuvchi emailiga yuborildi!")
            return redirect("reset_password")
    else:
        form = ForgotPasswordForm()

    return render(request, "accound/forgot_password.html", {"form": form})


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            old_pass = form.cleaned_data["old_pass"]
            new_pass = form.cleaned_data["new_pass"]
            confirm_pass = form.cleaned_data["confirm_pass"]

            username = request.session.get("reset_username")
            code_created_ts = request.session.get("code_created")

            if not code_created_ts or not username:
                messages.error(request, "❌ Kod mavjud emas, qayta yuboring!")
                return redirect("forgot_password")

            code_created = datetime.fromtimestamp(code_created_ts)
            if datetime.now() > code_created + timedelta(minutes=2):
                messages.error(request, "⌛ Kod muddati tugadi, qayta yuboring!")
                return redirect("forgot_password")

            if code != request.session.get("pass_code"):
                messages.error(request, "❌ Kod noto‘g‘ri!")
                return redirect("reset_password")

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "❌ Foydalanuvchi topilmadi!")
                return redirect("forgot_password")

            if not user.check_password(old_pass):
                messages.error(request, "❌ Eski parol noto‘g‘ri!")
                return redirect("reset_password")

            if new_pass != confirm_pass:
                messages.error(request, "❌ Yangi parol mos emas!")
                return redirect("reset_password")

            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request, user)

            for key in ["pass_code", "reset_username", "code_created"]:
                request.session.pop(key, None)

            messages.success(request, "✅ Parol muvaffaqiyatli o‘zgartirildi!")
            return redirect("login")
    else:
        form = ResetPasswordForm()

    return render(request, "accound/reset_password.html", {"form": form})
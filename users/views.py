from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm,ForgotPasswordForm,ResetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from .utils import generate_code, send_to_mail
from .models import CustomUser
from django.contrib.auth import get_user_model
from .forms import ProfileForm, CustomPasswordChangeForm

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

def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "Bunday username bazada mavjud emas")
                return render(request, "forgot_password.html", {"form": form})

            code = generate_code()
            request.session["reset_code"] = code
            request.session["reset_user"] = user.id
            request.session["reset_code_time"] = timezone.now().timestamp()
            send_to_mail(user.email, code)
            print(code)
            messages.success(request, "Kod sizning email manzilingizga yuborildi (2 daqiqa ichida amal qiladi)")
            return redirect("reset_password")
    else:
        form = ForgotPasswordForm()
    return render(request, "accound/forgot_password.html", {"form": form})


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            new_pass = form.cleaned_data["new_pass"]
            confirm_pass = form.cleaned_data["confirm_pass"]

            if "reset_code" not in request.session or "reset_user" not in request.session:
                messages.error(request, "Avval username kiritib kodni oling")
                return redirect("forgot_password")

            code_time = request.session.get("reset_code_time")
            if code_time is None or timezone.now().timestamp() - code_time > 120:
                messages.error(request, "Kod muddati tugagan, iltimos yangi kod oling")
                return redirect("forgot_password")

            if code != request.session["reset_code"]:
                messages.error(request, "Kod xato kiritildi")
                return render(request, "accound/reset_password.html", {"form": form})

            if new_pass != confirm_pass:
                messages.error(request, "Parollar mos kelmadi")
                return render(request, "accound/reset_password.html", {"form": form})

            # Hamma narsa to'g'ri bo'lsa parolni o'zgartirish
            user_id = request.session["reset_user"]
            user = User.objects.get(id=user_id)
            user.set_password(new_pass)
            user.save()

            # Session ma'lumotlarini tozalash
            del request.session["reset_code"]
            del request.session["reset_user"]
            del request.session["reset_code_time"]

            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi")
            return redirect("login")
    else:
        form = ResetPasswordForm()
    return render(request, "accound/reset_password.html", {"form": form})


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST" and "update_profile" in request.POST:
        profile_form = ProfileForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi")
            return redirect("profile")
    else:
        profile_form = ProfileForm(instance=user)

    if request.method == "POST" and "change_password" in request.POST:
        password_form = CustomPasswordChangeForm(request.POST)
        if password_form.is_valid():
            old_pass = password_form.cleaned_data["old_password"]
            new_pass = password_form.cleaned_data["new_password"]
            confirm_pass = password_form.cleaned_data["confirm_password"]

            if not user.check_password(old_pass):
                messages.error(request, "Eski parol noto‘g‘ri")
            elif old_pass == new_pass:
                messages.error(request, "Eski va yangi parol bir xil bo‘lishi mumkin emas")
            elif new_pass != confirm_pass:
                messages.error(request, "Yangi parol va tasdiqlash paroli mos kelmadi")
            else:
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Parol muvaffaqiyatli o‘zgartirildi")
                return redirect("profile")
    else:
        password_form = CustomPasswordChangeForm()

    context = {
        "profile_form": profile_form,
        "password_form": password_form,
        "user": user
    }
    return render(request, "accound/profile.html", context)
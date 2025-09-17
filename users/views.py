from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ChangePassForm, ResetPassForm
from .utils import generate_code, send_to_mail
from .models import CustomUser

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
            return redirect("index")
    else:
        form = LoginForm()
    return render(request, "accound/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("accound/login")




@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data["old_pass"]
            new_pass = form.cleaned_data["new_pass"]
            confirm_pass = form.cleaned_data["confirm_pass"]
            code = form.cleaned_data["code"]

            if not request.user.check_password(old_pass):
                messages.error(request, "Eski parol noto‘g‘ri!")
                return redirect("change_password")

            if new_pass != confirm_pass:
                messages.error(request, "Yangi parol mos emas!")
                return redirect("change_password")

            if code != request.session.get("pass_code"):
                messages.error(request, "Kod noto‘g‘ri!")
                return redirect("change_password")

            request.user.set_password(new_pass)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Parol muvaffaqiyatli o‘zgartirildi!")
            return redirect("profile")
    else:
        form = ChangePassForm()
        code = generate_code()
        request.session["pass_code"] = code
        send_to_mail(request.user.email, code)

    return render(request, "change_password.html", {"form": form})



def reset_password(request):
    if request.method == "POST":
        form = ResetPassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            code = form.cleaned_data["code"]

            if code != request.session.get("reset_code"):
                messages.error(request, "Kod noto‘g‘ri!")
                return redirect("reset_password")

            email = request.session.get("reset_email")
            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(password)
                user.save()
                messages.success(request, "Parol tiklandi, endi login qiling!")
                request.session.pop("reset_code", None)
                request.session.pop("reset_email", None)
                return redirect("login")
            except CustomUser.DoesNotExist:
                messages.error(request, "Bunday foydalanuvchi topilmadi!")
                return redirect("reset_password")
    else:
        form = ResetPassForm()
        email = request.GET.get("email")
        if email:
            code = generate_code()
            request.session["reset_code"] = code
            request.session["reset_email"] = email
            send_to_mail(email, code)

    return render(request, "accound/reset_password.html", {"form": form})
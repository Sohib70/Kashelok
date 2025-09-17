from django.urls import path
from .views import signup_view, login_view, logout_view,reset_password

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("reset-password/", reset_password, name="reset_password"),
]
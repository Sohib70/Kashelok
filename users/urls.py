from django.urls import path
from .views import signup_view, login_view, logout_view,forgot_password,reset_password,profile_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path("profile/",profile_view, name="profile"),
]
from django.urls import path
from .views import get_home

urlpatterns = [
    path('index/',get_home,name='index')
]
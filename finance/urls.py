from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    # kirim
    path("incomes/", views.income_list, name="income_list"),
    path("incomes/add/", views.income_create, name="income_create"),

    # chiqim
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/add/", views.expense_create, name="expense_create"),

    path("chart-data/", views.chart_data, name="chart_data"),

    path("kirim/", views.kirim_list, name="kirim_list"),
    path("chiqim/", views.chiqim_list, name="chiqim_list"),
]
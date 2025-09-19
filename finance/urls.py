from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    path("categories/", views.category_list, name="category_list"),
    path("add-category/", views.add_category, name="add_category"),
    path('categories/<int:pk>/edit/', views.update_category, name='update_category'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path("add-income/<int:pk>/", views.add_income, name="add_income"),

    path("expense-categories/", views.expense_category_list, name="expense_category_list"),
    path("add-expense-category/", views.add_expense_category, name="add_expense_category"),
    path('expense-categories/<int:pk_e>/edit/', views.update_expense_category, name='update_expense_category'),
    path('expense-categories/<int:pk_e>/', views.expense_category_detail, name='expense_category_detail'),
    path('expense-categories/<int:pk_e>/delete/', views.delete_expense_category, name='delete_expense_category'),
    path("add-expense/<int:pk_e>/", views.add_expense, name="add_expense"),

    path('income/<int:pk>/edit/', views.update_income, name='update_income'),
    path('income/<int:pk>/delete/', views.delete_income, name='delete_income'),

    path('expense/<int:pk>/edit/', views.update_expense, name='update_expense'),
    path('expense/<int:pk>/delete/', views.delete_expense, name='delete_expense'),

    path("update-balance/", views.update_balance, name="update_balance"),
]


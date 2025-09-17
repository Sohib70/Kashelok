from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date, timedelta
from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.dateparse import parse_date

def kirim_list(request):
    return render(request, "finance/kirim_list.html")

def chiqim_list(request):
    return render(request, "finance/chiqim_list.html")

@login_required
def dashboard(request):
    today = date.today()
    start_week = today - timedelta(days=today.weekday())  # haftaning 1-kuni
    start_month = today.replace(day=1)  # oyning 1-kuni

    # umumiy hisob
    total_income = Income.objects.filter(user=request.user).aggregate(Sum("amount"))["amount__sum"] or 0
    total_expense = Expense.objects.filter(user=request.user).aggregate(Sum("amount"))["amount__sum"] or 0
    balance = total_income - total_expense

    # kunlik
    daily_income = Income.objects.filter(user=request.user, date=today).aggregate(Sum("amount"))["amount__sum"] or 0
    daily_expense = Expense.objects.filter(user=request.user, date=today).aggregate(Sum("amount"))["amount__sum"] or 0

    # haftalik
    weekly_income = Income.objects.filter(user=request.user, date__gte=start_week).aggregate(Sum("amount"))["amount__sum"] or 0
    weekly_expense = Expense.objects.filter(user=request.user, date__gte=start_week).aggregate(Sum("amount"))["amount__sum"] or 0

    # oylik
    monthly_income = Income.objects.filter(user=request.user, date__gte=start_month).aggregate(Sum("amount"))["amount__sum"] or 0
    monthly_expense = Expense.objects.filter(user=request.user, date__gte=start_month).aggregate(Sum("amount"))["amount__sum"] or 0

    # sanalar oralig‘i bo‘yicha filter
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    filtered_income = filtered_expense = None

    if start_date and end_date:
        filtered_income = Income.objects.filter(user=request.user, date__range=[start_date, end_date])
        filtered_expense = Expense.objects.filter(user=request.user, date__range=[start_date, end_date])

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "daily_income": daily_income,
        "daily_expense": daily_expense,
        "weekly_income": weekly_income,
        "weekly_expense": weekly_expense,
        "monthly_income": monthly_income,
        "monthly_expense": monthly_expense,
        "filtered_income": filtered_income,
        "filtered_expense": filtered_expense,
    }
    return render(request, "dashboard.html", context)


@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by("-date")
    if request.method == "POST":
        form = IncomeForm(request.POST, request.FILES)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect("income_list")
    else:
        form = IncomeForm()
    return render(request, "finance/income_list.html", {"incomes": incomes, "form": form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "finance/expense_list.html", {"expenses": expenses, "form": form})


@login_required
def chart_data(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        incomes = Income.objects.filter(user=request.user, date__range=[start, end])
        expenses = Expense.objects.filter(user=request.user, date__range=[start, end])
    else:
        incomes = Income.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user)

    # Sana bo‘yicha guruhlash
    data = {}
    for inc in incomes:
        data.setdefault(str(inc.date), {"income": 0, "expense": 0})
        data[str(inc.date)]["income"] += float(inc.amount)

    for exp in expenses:
        data.setdefault(str(exp.date), {"income": 0, "expense": 0})
        data[str(exp.date)]["expense"] += float(exp.amount)

    labels = sorted(data.keys())
    income_data = [data[d]["income"] for d in labels]
    expense_data = [data[d]["expense"] for d in labels]

    return JsonResponse({
        "labels": labels,
        "income_data": income_data,
        "expense_data": expense_data
    })

@login_required
def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST, request.FILES)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect("income_list")  # qo‘shilgandan keyin ro‘yxatga qaytadi
    else:
        form = IncomeForm()
    return render(request, "finance/income_form.html", {"form": form})


# ---------------- Chiqim qo‘shish ----------------
@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()
    return render(request, "finance/expense_form.html", {"form": form})
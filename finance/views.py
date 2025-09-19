from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Income, Expense, Category, ExpenseCategory, UserBalance
from .forms import IncomeForm, CategoryForm, ExpenseCategoryForm, ExpenseForm
from datetime import datetime, timedelta
from decimal import Decimal

@login_required
def dashboard(request):
    user = request.user
    balance_obj, created = UserBalance.objects.get_or_create(user=user)

    dollar_to_sum = 12300

    if request.method == "POST":
        cash = request.POST.get("cash")
        card = request.POST.get("card")
        dollar = request.POST.get("dollar")
        balance_obj.cash = cash or 0
        balance_obj.card = card or 0
        balance_obj.dollar = dollar or 0
        balance_obj.save()
        return redirect("dashboard")

    period = request.GET.get('period', 'kunlik')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    today = datetime.today().date()
    if not start_date:
        start_date = today
    else:
        start_date = datetime.fromisoformat(start_date).date()
    if not end_date:
        end_date = start_date
    else:
        end_date = datetime.fromisoformat(end_date).date()

    if period == 'kunlik':
        start_date = end_date = start_date
    elif period == 'haftalik':
        start_date = end_date - timedelta(days=6)
    elif period == 'oylik':
        start_date = end_date.replace(day=1)

    kirimlar = Income.objects.filter(user=user, date__range=[start_date, end_date])
    chiqimlar = Expense.objects.filter(user=user, date__range=[start_date, end_date])

    kirim_sum = kirimlar.aggregate(total=Sum('amount'))['total'] or 0
    chiqim_sum = chiqimlar.aggregate(total=Sum('amount'))['total'] or 0
    balance = kirim_sum - chiqim_sum

    income_categories = []
    for cat in Category.objects.all():
        total = kirimlar.filter(category=cat).aggregate(total=Sum('amount'))['total'] or 0
        if total > 0:
            cat.sum = total
            cat.icon = getattr(cat, 'image', '')
            income_categories.append(cat)

    expense_categories = []
    for cat in ExpenseCategory.objects.all():
        total = chiqimlar.filter(category=cat).aggregate(total=Sum('amount'))['total'] or 0
        if total > 0:
            cat.sum = total
            cat.icon = getattr(cat, 'image', '')
            expense_categories.append(cat)

    total_balance = balance_obj.total_balance(dollar_to_sum=dollar_to_sum) + balance

    context = {
        'kirim_sum': kirim_sum,
        'chiqim_sum': chiqim_sum,
        'balance': balance,
        'income_categories': income_categories,
        'expense_categories': expense_categories,
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
        'cash_amount': balance_obj.cash,
        'card_amount': balance_obj.card,
        'dollar_amount': balance_obj.dollar,
        'dollar_to_sum': dollar_to_sum,
        'total_balance': total_balance,
    }
    return render(request, 'dashboard.html', context)


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    for cat in categories:
        cat.total_income = cat.income_set.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, "category_list.html", {"categories": categories})

@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    incomes = category.income_set.filter(user=request.user)
    return render(request, "category_detail.html", {"category": category, "incomes": incomes})

@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})

@login_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya yangilandi")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "add_category.html", {"form": form})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Kategoriya o‘chirildi")
        return redirect("category_list")
    return render(request, "delete_category.html", {"category": category})


@login_required
def expense_category_list(request):
    categories = ExpenseCategory.objects.filter(user=request.user)
    for cat in categories:
        cat.total_expense = cat.expense_set.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, "expense_category_list.html", {"categories": categories})

@login_required
def expense_category_detail(request, pk_e):
    category = get_object_or_404(ExpenseCategory, pk=pk_e)
    expenses = category.expense_set.filter(user=request.user)
    return render(request, "expense_category_detail.html", {"category": category, "expenses": expenses})

@login_required
def add_expense_category(request):
    if request.method == "POST":
        form = ExpenseCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Chiqim kategoriyasi qo‘shildi")
            return redirect("expense_category_list")
    else:
        form = ExpenseCategoryForm()
    return render(request, "add_expense_category.html", {"form": form})

@login_required
def update_expense_category(request, pk_e):
    category = get_object_or_404(ExpenseCategory, pk=pk_e)
    if request.method == "POST":
        form = ExpenseCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Chiqim kategoriyasi yangilandi")
            return redirect("expense_category_list")
    else:
        form = ExpenseCategoryForm(instance=category)
    return render(request, "add_expense_category.html", {"form": form})

@login_required
def delete_expense_category(request, pk_e):
    category = get_object_or_404(ExpenseCategory, pk=pk_e)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Chiqim kategoriyasi o‘chirildi")
        return redirect("expense_category_list")
    return render(request, "delete_expense_category.html", {"category": category})


@login_required
def add_income(request, pk=None):
    category = None
    if pk:
        category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            if category:
                income.category = category
            income.save()

            balance_obj, created = UserBalance.objects.get_or_create(user=request.user)
            if income.payment_method == 'cash':
                balance_obj.cash += Decimal(income.amount)
            elif income.payment_method == 'card':
                balance_obj.card += Decimal(income.amount)
            elif income.payment_method == 'dollar':
                balance_obj.dollar += Decimal(income.amount)
            balance_obj.save()

            messages.success(request, "Kirim qo‘shildi va balans yangilandi")
            return redirect('category_detail', pk=income.category.id)
    else:
        form = IncomeForm(initial={"category": category})
    return render(request, "add_income.html", {"form": form, "category": category})


@login_required
def update_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        old_amount = income.amount
        old_method = income.payment_method
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            balance_obj, created = UserBalance.objects.get_or_create(user=request.user)
            if old_method == 'cash':
                balance_obj.cash -= old_amount
            elif old_method == 'card':
                balance_obj.card -= old_amount
            elif old_method == 'dollar':
                balance_obj.dollar -= old_amount
            if income.payment_method == 'cash':
                balance_obj.cash += income.amount
            elif income.payment_method == 'card':
                balance_obj.card += income.amount
            elif income.payment_method == 'dollar':
                balance_obj.dollar += income.amount
            balance_obj.save()

            messages.success(request, "Kirim yangilandi va balans tuzatildi")
            return redirect('category_detail', pk=income.category.id)
    else:
        form = IncomeForm(instance=income)
    return render(request, "add_income.html", {"form": form, "category": income.category})


@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        balance_obj, created = UserBalance.objects.get_or_create(user=request.user)
        if income.payment_method == 'cash':
            balance_obj.cash -= income.amount
        elif income.payment_method == 'card':
            balance_obj.card -= income.amount
        elif income.payment_method == 'dollar':
            balance_obj.dollar -= income.amount
        balance_obj.save()

        category_id = income.category.id
        income.delete()
        messages.success(request, "Kirim o‘chirildi va balans tuzatildi")
        return redirect('category_detail', pk=category_id)
    return render(request, "delete_income.html", {"income": income})


@login_required
def add_expense(request, pk_e=None):
    category = None
    if pk_e:
        category = get_object_or_404(ExpenseCategory, pk=pk_e)

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            if category:
                expense.category = category
            elif not expense.category:
                messages.error(request, "Kategoriya tanlanmagan")
                return redirect('expense_category_list')

            expense.save()

            balance_obj, created = UserBalance.objects.get_or_create(user=request.user)

            amount = Decimal(expense.amount)

            if expense.payment_method == 'cash':
                balance_obj.cash -= amount
            elif expense.payment_method == 'card':
                balance_obj.card -= amount
            elif expense.payment_method == 'dollar':
                balance_obj.dollar -= amount

            balance_obj.save()

            messages.success(request, "Chiqim qo‘shildi va balans yangilandi")
            return redirect('expense_category_detail', pk_e=expense.category.id)
    else:
        form = ExpenseForm(initial={"category": category})

    return render(request, "add_expense.html", {"form": form, "category": category})


@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        old_amount = expense.amount
        old_method = expense.payment_method
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            balance_obj, created = UserBalance.objects.get_or_create(user=request.user)
            if old_method == 'cash':
                balance_obj.cash += old_amount
            elif old_method == 'card':
                balance_obj.card += old_amount
            elif old_method == 'dollar':
                balance_obj.dollar += old_amount
            if expense.payment_method == 'cash':
                balance_obj.cash -= expense.amount
            elif expense.payment_method == 'card':
                balance_obj.card -= expense.amount
            elif expense.payment_method == 'dollar':
                balance_obj.dollar -= expense.amount
            balance_obj.save()

            messages.success(request, "Chiqim yangilandi va balans tuzatildi")
            return redirect('expense_category_detail', pk_e=expense.category.id)
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "add_expense.html", {"form": form, "category": expense.category})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        balance_obj, created = UserBalance.objects.get_or_create(user=request.user)
        if expense.payment_method == 'cash':
            balance_obj.cash += expense.amount
        elif expense.payment_method == 'card':
            balance_obj.card += expense.amount
        elif expense.payment_method == 'dollar':
            balance_obj.dollar += expense.amount
        balance_obj.save()

        category_id = expense.category.id
        expense.delete()
        messages.success(request, "Chiqim o‘chirildi va balans tuzatildi")
        return redirect('expense_category_detail', pk_e=category_id)
    return render(request, "delete_expense.html", {"expense": expense})


@login_required
def update_balance(request):
    balance_obj, created = UserBalance.objects.get_or_create(user=request.user)

    if request.method == "POST":
        cash = request.POST.get("cash") or 0
        card = request.POST.get("card") or 0
        dollar = request.POST.get("dollar") or 0

        balance_obj.cash = Decimal(cash)
        balance_obj.card = Decimal(card)
        balance_obj.dollar = Decimal(dollar)
        balance_obj.save()

        messages.success(request, "Balans yangilandi")
        return redirect("dashboard")

    return redirect("dashboard")
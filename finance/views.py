from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Income, Expense, Category, ExpenseCategory
from .forms import IncomeForm, CategoryForm, ExpenseCategoryForm, ExpenseForm

# ---------------- Dashboard ----------------
@login_required
def dashboard(request):
    user = request.user

    # Kirimlar
    kirimlar = Income.objects.filter(user=user)
    kirim_sum = kirimlar.aggregate(total=Sum('amount'))['total'] or 0
    income_categories = Category.objects.all()
    income_cat_list = []
    for cat in income_categories:
        cat_sum = kirimlar.filter(category=cat).aggregate(total=Sum('amount'))['total'] or 0
        cat.icon = getattr(cat, 'image', '')
        cat.sum = cat_sum
        income_cat_list.append(cat)

    # Chiqimlar
    chiqimlar = Expense.objects.filter(user=user)
    chiqim_sum = chiqimlar.aggregate(total=Sum('amount'))['total'] or 0
    expense_categories = ExpenseCategory.objects.all()
    expense_cat_list = []
    for cat in expense_categories:
        cat_sum = chiqimlar.filter(category=cat).aggregate(total=Sum('amount'))['total'] or 0
        cat.icon = getattr(cat, 'image', '')
        cat.sum = cat_sum
        expense_cat_list.append(cat)

    balance = kirim_sum - chiqim_sum

    context = {
        'kirim_sum': kirim_sum,
        'chiqim_sum': chiqim_sum,
        'balance': balance,
        'income_categories': income_cat_list,
        'expense_categories': expense_cat_list,
    }
    return render(request, 'dashboard.html', context)


# ---------------- Category Views (Income) ----------------
@login_required
def category_list(request):
    categories = Category.objects.all()
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


# ---------------- ExpenseCategory Views ----------------
@login_required
def expense_category_list(request):
    categories = ExpenseCategory.objects.all()
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


# ---------------- Income Views ----------------
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
            messages.success(request, "Kirim qo‘shildi")
            return redirect('category_detail', pk=income.category.id)
    else:
        form = IncomeForm(initial={"category": category})
    return render(request, "add_income.html", {"form": form, "category": category})

@login_required
def update_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "Kirim yangilandi")
            return redirect('category_detail', pk=income.category.id)
    else:
        form = IncomeForm(instance=income)
    return render(request, "add_income.html", {"form": form, "category": income.category})

@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        category_id = income.category.id
        income.delete()
        messages.success(request, "Kirim o‘chirildi")
        return redirect('category_detail', pk=category_id)
    return render(request, "delete_income.html", {"income": income})


# ---------------- Expense Views ----------------
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
            messages.success(request, "Chiqim qo‘shildi")
            return redirect('expense_category_detail', pk_e=expense.category.id)
    else:
        form = ExpenseForm(initial={"category": category})

    return render(request, "add_expense.html", {"form": form, "category": category})

@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Chiqim yangilandi")
            return redirect('expense_category_detail', pk_e=expense.category.id)
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "add_expense.html", {"form": form, "category": expense.category})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        category_id = expense.category.id
        expense.delete()
        messages.success(request, "Chiqim o‘chirildi")
        return redirect('expense_category_detail', pk_e=category_id)
    return render(request, "delete_expense.html", {"expense": expense})

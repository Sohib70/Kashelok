from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Income, Expense, Category,ExpenseCategory
from .forms import IncomeForm,CategoryForm,ExpenseCategoryForm,ExpenseForm
from django.contrib import messages


@login_required
def dashboard(request):
    user = request.user

    kirimlar = Income.objects.filter(user=user)
    kirim_sum = kirimlar.aggregate(total=Sum('amount'))['total'] or 0

    chiqimlar = Expense.objects.filter(user=user)
    chiqim_sum = chiqimlar.aggregate(total=Sum('amount'))['total'] or 0

    balance = kirim_sum - chiqim_sum

    categories = Category.objects.all()
    cat_list = []
    for cat in categories:
        cat_sum = chiqimlar.filter(category=cat).aggregate(total=Sum('amount'))['total'] or 0
        cat.icon = getattr(cat, 'icon', '')
        cat.sum = cat_sum
        cat_list.append(cat)

    context = {
        'kirim_sum': kirim_sum,
        'chiqim_sum': chiqim_sum,
        'balance': balance,
        'categories': cat_list,
    }

    return render(request, 'dashboard.html', context)


@login_required
def category_list(request):
    categories = Category.objects.all()
    for cat in categories:
        cat.total_income = cat.income_set.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, "category_list.html", {"categories": categories})

@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    incomes = category.income_set.all()
    return render(request, "category_detail.html", {
        "category": category,
        "incomes": incomes
    })


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
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
    categories = ExpenseCategory.objects.all()
    for cat in categories:
        cat.total_expense = cat.expense_set.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, "expense_category_list.html", {"categories": categories})

@login_required
def expense_category_detail(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    expenses = category.expense_set.filter(user=request.user)
    return render(request, "expense_category_detail.html", {
        "category": category,
        "expenses": expenses
    })

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
def update_expense_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
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
def delete_expense_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Chiqim kategoriyasi o‘chirildi")
        return redirect("expense_category_list")
    return render(request, "delete_expense_category.html", {"category": category})



@login_required
def add_income(request, category_id=None):
    category = None
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
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



@login_required
def add_expense(request, category_id=None):
    category = None
    if category_id:
        category = get_object_or_404(ExpenseCategory, pk=category_id)

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
            return redirect('expense_category_detail', pk=expense.category.id)
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
            return redirect('expense_category_detail', pk=expense.category.id)
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
        return redirect('expense_category_detail', pk=category_id)
    return render(request, "delete_expense.html", {"expense": expense})



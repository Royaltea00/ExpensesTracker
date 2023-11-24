from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from main.models import Expense, Category


# Create your views here.
@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'home.html', {'expenses': expenses, 'categories': categories})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})


@login_required
def view_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    return render(request, 'view_expense.html', {'expense': expense})


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense edited successfully!')
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('home')

    return render(request, 'delete_expense.html', {'expense': expense})


@login_required
def monthly_summary(request):
    current_month_expenses = Expense.objects.filter(user=request.user, date__month__exact=1)

    return render(request, 'monthly_summary.html', {'current_month_expenses': current_month_expenses})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('home')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category edited successfully!')
            return redirect('home')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'edit_category.html', {'form': form, 'category': category})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('home')

    return render(request, 'delete_category.html', {'category': category})


@login_required
def user_dashboard(request):
    total_expenses = Expense.objects.filter(user=request.user).count()
    total_categories = Category.objects.count()

    return render(request, 'user_dashboard.html',
                  {'total_expenses': total_expenses, 'total_categories': total_categories})


@login_required
def user_profile(request):
    user_expenses = Expense.objects.filter(user=request.user)
    user_categories = Category.objects.filter(expense__user=request.user).distinct()

    return render(request, 'user_profile.html', {'user_expenses': user_expenses, 'user_categories': user_categories})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')

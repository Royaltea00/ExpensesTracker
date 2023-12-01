# from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractDay, ExtractYear
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Expense, Category, UserProfile
from django.contrib.auth.decorators import login_required

from .app_forms import ExpenseForm, CategoryForm, UserProfileForm, ChangePasswordForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


@login_required
def home(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user)
        return render(request, 'main/home.html', {'expenses': expenses, 'categories': categories})
    else:
        messages.error(request, 'You must be logged in to view this page.')
        return HttpResponseForbidden('You must be logged in to view this page.')


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'main/add_expense.html', {'form': form})


@login_required
def view_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    context = {'expense': expense}
    return render(request, 'main/view_expense.html', context)


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'main/edit_expense.html', {'form': form, 'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
        return redirect('home')
    return render(request, 'main/delete_expense.html', {'expense': expense})


@login_required
def monthly_summary(request):
    monthly_data = Expense.objects.filter(user=request.user).annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(total_amount=Sum('amount')).order_by('month')

    # Calculate total_expenses
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

    print("Monthly Data:", monthly_data)

    return render(request, 'main/monthly_summary.html', {'monthly_data': monthly_data, 'total_expenses': total_expenses})


@login_required
def weekly_summary(request):
    weekly_data = Expense.objects.filter(user=request.user).annotate(
        week=ExtractWeek('date')
    ).values('week').annotate(total_amount=Sum('amount')).order_by('week')

    # Calculate total_expenses
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

    print("Weekly Data:", weekly_data)

    return render(request, 'main/weekly_summary.html', {'weekly_data': weekly_data, 'total_expenses': total_expenses})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully.')
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'main/add_category.html', {'form': form})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('home')
    return render(request, 'main/delete_category.html', {'category': category})


@login_required
def user_dashboard(request):
    user_expenses = Expense.objects.filter(user=request.user)
    total_expenses = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    expense_count = user_expenses.count()
    context = {
        'total_expenses': total_expenses,
        'expense_count': expense_count,
        'user_expenses': user_expenses,
    }
    return render(request, 'main/user_dashboard.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'main/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('user_profile')
    else:
        form = ChangePasswordForm()
    return render(request, 'main/change_password.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')


@login_required
def user_profile(request):
    user = request.user
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        # Create UserProfile for the user if it doesn't exist
        UserProfile.objects.create(user=user)
        user_profile = user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
        else:
            messages.error(request, 'There was an error updating your profile. Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'main/user_profile.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for the new user
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def daily_summary(request):
    daily_data = Expense.objects.filter(user=request.user).annotate(
        day=ExtractDay('date')
    ).values('day').annotate(total_amount=Sum('amount')).order_by('day')

    # Calculate total_expenses
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total_expenses=Sum('amount'))[
                         'total_expenses'] or 0

    print("Daily Data:", daily_data)

    return render(request, 'main/daily_summary.html', {'daily_data': daily_data, 'total_expenses': total_expenses})


@login_required
def yearly_summary(request):
    yearly_data = Expense.objects.filter(user=request.user).annotate(
        year=ExtractYear('date')
    ).values('year').annotate(total_amount=Sum('amount')).order_by('year')

    # Calculate total_expenses
    total_expenses = Expense.objects.filter(user=request.user).aggregate(total_expenses=Sum('amount'))[
                         'total_expenses'] or 0

    print("Yearly Data:", yearly_data)

    return render(request, 'main/yearly_summary.html', {'yearly_data': yearly_data, 'total_expenses': total_expenses})

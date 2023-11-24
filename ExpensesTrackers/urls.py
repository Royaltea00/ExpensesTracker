"""
URL configuration for ExpensesTrackers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.views import user_login, user_logout, home, add_expense, view_expense, delete_expense, edit_expense, \
    monthly_summary, add_category, edit_category, delete_category, user_dashboard, user_profile

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    path('add_expense/', add_expense, name='add_expense'),
    path('expense/<int:expense_id>/', view_expense, name='view_expense'),
    path('expense/<int:expense_id>/edit/', edit_expense, name='edit_expense'),
    path('expense/<int:expense_id>/delete/', delete_expense, name='delete_expense'),
    path('monthly_summary/', monthly_summary, name='monthly_summary'),
    path('add_category/', add_category, name='add_category'),
    path('category/<int:category_id>/edit/', edit_category, name='edit_category'),
    path('category/<int:category_id>/delete/', delete_category, name='delete_category'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('user_profile/', user_profile, name='user_profile'),
    path('admin/', admin.site.urls),
]

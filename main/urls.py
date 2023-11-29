
from django.contrib.auth import views as auth_views

from django.urls import path

from main.views import user_logout, home, add_expense, view_expense, delete_expense, monthly_summary, \
    weekly_summary, add_category, delete_category, user_dashboard, user_profile, edit_profile, \
    CustomLoginView, signup, change_password, yearly_summary, daily_summary

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('', home, name='home'),
    path('add_expense/', add_expense, name='add_expense'),
    path('expense/<int:expense_id>/', view_expense, name='view_expense'),
    path('expense/<int:expense_id>/delete/', delete_expense, name='delete_expense'),
    path('monthly_summary/', monthly_summary, name='monthly_summary'),
    path('weekly_summary/', weekly_summary, name='weekly_summary'),
    path('add_category/', add_category, name='add_category'),
    path('change_password/', change_password, name='change_password'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('category/<int:category_id>/delete/', delete_category, name='delete_category'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('user_profile/', user_profile, name='user_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('daily_summary/', daily_summary, name='daily_summary'),
    path('yearly_summary/', yearly_summary, name='yearly_summary'),
]

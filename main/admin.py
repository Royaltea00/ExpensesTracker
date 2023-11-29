from django.contrib import admin
from .models import Expense, Category, WeeklySummary, MonthlySummary, UserProfile, DailySummary, YearlySummary

# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(WeeklySummary)
admin.site.register(MonthlySummary)
admin.site.register(UserProfile)
admin.site.register(DailySummary)
admin.site.register(YearlySummary)


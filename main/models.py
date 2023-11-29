from django.db import models
from django.contrib.auth.models import User
# from django.db.models import Sum
# from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractDay, ExtractYear


class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.description


class WeeklySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateTimeField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Weekly Summary for {self.user.username}"


class MonthlySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month_start = models.DateTimeField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Monthly Summary for {self.user.username}"


class DailySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_start = models.DateTimeField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Daily Summary for {self.user.username}"


class YearlySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year_start = models.DateTimeField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Yearly Summary for {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

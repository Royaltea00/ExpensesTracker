# main/management/commands/populate.py

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from main.models import Expense, Category, WeeklySummary, MonthlySummary, DailySummary, YearlySummary
import random
from faker import Faker
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate the database with dummy data'
    fake = Faker()

    def handle(self, *args, **options):
        try:
            # Clear existing data
            User.objects.all().delete()
            Expense.objects.all().delete()
            Category.objects.all().delete()
            DailySummary.objects.all().delete()
            WeeklySummary.objects.all().delete()
            MonthlySummary.objects.all().delete()
            YearlySummary.objects.all().delete()

            # Create users
            users = []
            for _ in range(15):
                user = User.objects.create_user(
                    username=self.fake.user_name(),
                    password="password",
                    email=self.fake.email()
                )
                users.append(user)

            # Create categories
            categories = []
            for _ in range(5):
                category = Category.objects.create(
                    name=self.fake.word(),
                    user=random.choice(users)
                )
                categories.append(category)

            # Create expenses
            for _ in range(20):
                expense = Expense.objects.create(
                    amount=random.uniform(10, 100),
                    description=self.fake.text(),
                    category=random.choice(categories),
                    user=random.choice(users),
                    date=datetime.now() - timedelta(days=random.randint(0, 365))
                )

            # Create weekly summaries
            for user in users:
                WeeklySummary.objects.create(
                    user=user,
                    week_start=datetime.now() - timedelta(days=random.randint(0, 365)),
                    total_expenses=random.uniform(500, 5000),
                    description=self.fake.text(),
                    date=datetime.now() - timedelta(days=random.randint(0, 365))
                )

            # Create monthly summaries
            for user in users:
                MonthlySummary.objects.create(
                    user=user,
                    month_start=datetime.now() - timedelta(days=random.randint(0, 365)),
                    total_expenses=random.uniform(10000, 200000),
                    description=self.fake.text(),
                    date=datetime.now() - timedelta(days=random.randint(0, 365))
                )

            # Create daily summaries
            for user in users:
                DailySummary.objects.create(
                    user=user,
                    day_start=datetime.now() - timedelta(days=random.randint(0, 365)),
                    total_expenses=random.uniform(1000, 10000),
                    description=self.fake.text(),
                    date=datetime.now() - timedelta(days=random.randint(0, 365))
                )

            # Create yearly summaries
            for user in users:
                YearlySummary.objects.create(
                    user=user,
                    year_start=datetime.now() - timedelta(days=random.randint(0, 365)),
                    total_expenses=random.uniform(50000, 200000),
                    description=self.fake.text(),
                    date=datetime.now() - timedelta(days=random.randint(0, 365))
                )

            self.stdout.write(self.style.SUCCESS('Database populated successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

# Generated by Django 4.2.7 on 2023-11-29 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_category_user_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

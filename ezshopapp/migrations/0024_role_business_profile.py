# Generated by Django 4.1.13 on 2024-03-16 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0023_dayclosingadmin_employee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='business_profile',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
    ]

# Generated by Django 4.1.13 on 2024-02-29 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0029_rename_employee_transaction_id_employee_employee_transaction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='employee_transaction',
        ),
    ]
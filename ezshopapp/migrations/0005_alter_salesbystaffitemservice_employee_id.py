# Generated by Django 4.1.13 on 2024-03-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0004_salesbystaffitemservice_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesbystaffitemservice',
            name='employee_id',
            field=models.IntegerField(default='1', null=True, verbose_name='Employee ID'),
        ),
    ]

# Generated by Django 4.1.13 on 2024-03-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0003_alter_salebyadminservice_employee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='itemtotal',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Products Total'),
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='servicetotal',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Service Total'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='services',
            field=models.ManyToManyField(to='ezshopapp.service'),
        ),
        migrations.DeleteModel(
            name='SaleItem',
        ),
    ]

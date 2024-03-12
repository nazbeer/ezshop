# Generated by Django 4.1.13 on 2024-03-11 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0011_remove_sale_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesByStaffItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card')], max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.employee', verbose_name='Employee')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.product')),
            ],
        ),
    ]

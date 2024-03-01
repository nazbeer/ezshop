# Generated by Django 4.1.13 on 2024-02-13 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ezshopapp', '0009_remove_salesbyadminitem_tip'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesByStaffItemService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tip', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card')], max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.product')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.service')),
            ],
        ),
    ]
# Generated by Django 4.1.13 on 2024-02-13 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0010_salesbystaffitemservice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesbystaffitemservice',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='salesbystaffitemservice',
            name='item',
        ),
        migrations.RemoveField(
            model_name='salesbystaffitemservice',
            name='price',
        ),
        migrations.RemoveField(
            model_name='salesbystaffitemservice',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='salesbystaffitemservice',
            name='tip',
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='pprice',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Product Price'),
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='pquantity',
            field=models.PositiveIntegerField(null=True, verbose_name='Product Quantity'),
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='sprice',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Service Price'),
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='squantity',
            field=models.PositiveIntegerField(null=True, verbose_name='Service Quantity'),
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Sub Total'),
        ),
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Total Amount'),
        ),
        migrations.AlterField(
            model_name='salesbystaffitemservice',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='salesbystaffitemservice',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='salesbystaffitemservice',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('card', 'Card')], max_length=20, verbose_name='Payment Method'),
        ),
        migrations.AlterField(
            model_name='salesbystaffitemservice',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.service', verbose_name='Service'),
        ),
    ]
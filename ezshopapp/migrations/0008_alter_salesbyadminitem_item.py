# Generated by Django 4.1.13 on 2024-02-09 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0007_salesbyadminitem_discount_salesbyadminitem_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesbyadminitem',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.product'),
        ),
    ]
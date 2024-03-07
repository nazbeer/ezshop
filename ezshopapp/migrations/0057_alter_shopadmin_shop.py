# Generated by Django 4.1.13 on 2024-03-07 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0056_alter_shopadmin_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopadmin',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_users', to='ezshopapp.shop', verbose_name='Shop Name'),
        ),
    ]

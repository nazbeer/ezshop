# Generated by Django 4.1.13 on 2024-03-01 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0037_alter_businessprofile_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessprofile',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezshopapp.shop'),
        ),
    ]
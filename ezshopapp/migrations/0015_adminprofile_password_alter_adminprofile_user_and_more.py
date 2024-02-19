# Generated by Django 4.1.13 on 2024-02-19 00:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ezshopapp', '0014_alter_shopadmin_license_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='password',
            field=models.CharField(default='ezshop@2024', max_length=128),
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='businessprofile',
            name='shop_phone_number',
            field=models.CharField(max_length=25),
        ),
    ]

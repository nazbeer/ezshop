# Generated by Django 4.1.13 on 2024-03-19 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0025_alter_role_business_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='business_profile',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='business_profile',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

# Generated by Django 4.1.13 on 2024-05-06 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0002_bank_business_profile_bankdeposit_business_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensetype',
            name='business_profile',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='receipttype',
            name='business_profile',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
# Generated by Django 5.0.4 on 2024-05-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='business_profile',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bankdeposit',
            name='business_profile',
            field=models.CharField(max_length=255, null=True),
        ),
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
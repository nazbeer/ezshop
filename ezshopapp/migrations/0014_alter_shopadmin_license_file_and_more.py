# Generated by Django 4.1.13 on 2024-02-19 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0013_adminprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopadmin',
            name='license_file',
            field=models.FileField(upload_to='license/'),
        ),
        migrations.AlterField(
            model_name='shopadmin',
            name='vat_certificate',
            field=models.FileField(upload_to='vat_certificate/'),
        ),
    ]

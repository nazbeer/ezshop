# Generated by Django 4.1.13 on 2024-03-11 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0020_alter_dayclosingadmin_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayclosing',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='dayclosingadmin',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='approved', max_length=10),
        ),
    ]

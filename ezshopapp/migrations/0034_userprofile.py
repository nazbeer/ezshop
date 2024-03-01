# Generated by Django 4.1.13 on 2024-03-01 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0033_dayclosing_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profiles', to='ezshopapp.shop')),
            ],
        ),
    ]

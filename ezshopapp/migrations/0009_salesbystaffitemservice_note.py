# Generated by Django 5.0.4 on 2024-05-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0008_salebystaffservice_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesbystaffitemservice',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.4 on 2024-06-24 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezshopapp', '0011_alter_dailysummary_narration'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysummary',
            name='advance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]

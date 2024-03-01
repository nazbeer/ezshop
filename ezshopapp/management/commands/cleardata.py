# cleardata.py

from django.apps import apps
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Clears all data from all models in the ezshopapp application'

    def handle(self, *args, **kwargs):
        # Get all models from the ezshopapp application
        app_models = apps.get_app_config('ezshopapp').get_models()

        # Loop through each model and delete all records
        for model in app_models:
            model.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('All data cleared successfully.'))

from django.core.management.base import BaseCommand
from django.utils import timezone
from random import randint
from ezshopapp.models import DayClosing

class Command(BaseCommand):
    help = 'Create dummy data for DayClosing model'

    def handle(self, *args, **kwargs):
        # Create 10 dummy DayClosing instances
        for _ in range(10):
            DayClosing.objects.create(
                date=timezone.now().date(),
                total_services=randint(1, 100),
                total_sales=randint(1, 1000),
                tip=randint(0, 100),
                total_collection=randint(100, 1000),
                advance=randint(0, 500),
                net_collection=randint(100, 1000),
                status='pending'
            )
        self.stdout.write(self.style.SUCCESS('Dummy data created successfully.'))

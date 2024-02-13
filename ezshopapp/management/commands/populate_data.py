from django.core.management.base import BaseCommand
from django.utils import timezone
from random import randint
from ezshopapp.models import DayClosing, SaleByAdminService, SalesByAdminItem

class Command(BaseCommand):
    help = 'Create dummy data for DayClosing, SaleByAdminService, and SalesByAdminItem models'

    def handle(self, *args, **kwargs):
        try:
            # Create dummy data for DayClosing model
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

            # Create dummy data for SaleByAdminService model
            for _ in range(10):
                SaleByAdminService.objects.create(
                    date=timezone.now().date(),
                    employee_id=randint(1, 10),  # Assuming there are 10 employees
                    service_id=randint(1, 10),   # Assuming there are 10 services
                    quantity=randint(1, 10),
                    price=randint(10, 100),
                    discount=randint(0, 10),
                    tip=randint(0, 10),
                    payment_method='Cash'  # Assuming default payment method is Cash
                )

            # Create dummy data for SalesByAdminItem model
            for _ in range(10):
                SalesByAdminItem.objects.create(
                    date=timezone.now().date(),
                    employee_id=randint(1, 10),  # Assuming there are 10 employees
                    item_id=randint(1, 10),      # Assuming there are 10 products
                    quantity=randint(1, 10),
                    price=randint(10, 100),
                    discount=randint(0, 10),
                    tip=randint(0, 10),
                    payment_method='Cash'  # Assuming default payment method is Cash
                )

            self.stdout.write(self.style.SUCCESS('Dummy data created successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

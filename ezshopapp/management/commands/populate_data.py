from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ezshopapp.models import Shop, ShopAdmin
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Populate shops and shop admins'

    def handle(self, *args, **options):
        # Create 5 Shop instances
        shops = []
        for _ in range(5):
            shop = Shop.objects.create(
                name=fake.company(),
                license_number=fake.uuid4(),
                num_users=fake.random_int(),
                vat_remainder=fake.boolean(),
                employee_transaction_window=fake.boolean(),
                license_expiration_reminder=fake.boolean(),
                employee_visa_expiration_reminder=fake.boolean(),
                employee_passport_expiration_reminder=fake.boolean()
            )
            shops.append(shop)

        # Create ShopAdmin instances associated with the created shops
        for shop in shops:
            ShopAdmin.objects.create(
                shop=shop,
                license_expiration=fake.date_this_decade(),
                license_file=fake.file_name(),
                phone_number=fake.phone_number(),
                vat_percentage=fake.random_digit(),
                vat_number=fake.uuid4(),
                vat_submission_date=fake.date_this_decade(),
                vat_certificate=fake.file_name(),
                address=fake.address(),
                admin_user=User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password=fake.password()
                ),
                license_expiration_reminder_days=fake.random_int(),
                vat_submission_date_reminder_days=fake.random_int(),
                employee_visa_expiration_reminder_days=fake.random_int()
            )

        self.stdout.write(self.style.SUCCESS('Data populated successfully!'))

import random
from faker import Faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from ezshopapp.models import Shop, Role, Employee, ExpenseType, ReceiptTransaction, PaymentTransaction, BankDeposit, Service, Product, EmployeeTransaction, DailySummary

fake = Faker()

class Command(BaseCommand):
    help = 'Populate models with dummy data'

    def handle(self, *args, **options):
        self.populate_users()
        self.populate_shops()
        self.populate_roles()
        self.populate_employees()
        self.populate_expense_types()
        self.populate_receipt_transactions()
        self.populate_payment_transactions()
        self.populate_bank_deposits()
        self.populate_services()
        self.populate_products()
        self.populate_employee_transactions()
        self.populate_daily_summaries()
        self.stdout.write(self.style.SUCCESS('Successfully populated models with dummy data'))

    def populate_users(self):
        # Create a superuser for admin access
        User.objects.create_superuser('admin', 'admin@admin.com', '1234')

        # Create additional users if needed
        for _ in range(5):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            User.objects.create_user(username, email, password)

    def populate_shops(self):
        # Populate Shop model with dummy data
        for _ in range(10):
            Shop.objects.create(name=fake.company(), location=fake.address())

    def populate_roles(self):
        # Populate Role model with dummy data
        for _ in range(5):
            Role.objects.create(name=fake.job(), description=fake.text())

    def populate_employees(self):
        # Populate Employee model with dummy data
        for _ in range(20):
            Employee.objects.create(
                name=fake.name(),
                role=random.choice(Role.objects.all()),
                salary=random.uniform(30000, 80000),
                hire_date=fake.date_this_decade(),
            )

    def populate_expense_types(self):
        # Populate ExpenseType model with dummy data
        for _ in range(5):
            ExpenseType.objects.create(name=fake.word(), description=fake.text())

    def populate_receipt_transactions(self):
        # Populate ReceiptTransaction model with dummy data
        for _ in range(15):
            ReceiptTransaction.objects.create(
                amount=random.uniform(100, 1000),
                date=fake.date_this_year(),
                expense_type=random.choice(ExpenseType.objects.all()),
            )

    def populate_payment_transactions(self):
        # Populate PaymentTransaction model with dummy data
        for _ in range(15):
            PaymentTransaction.objects.create(
                amount=random.uniform(100, 1000),
                date=fake.date_this_year(),
            )

    def populate_bank_deposits(self):
        # Populate BankDeposit model with dummy data
        for _ in range(10):
            BankDeposit.objects.create(
                amount=random.uniform(5000, 20000),
                date=fake.date_this_year(),
            )

    def populate_services(self):
        # Populate Service model with dummy data
        for _ in range(10):
            Service.objects.create(name=fake.word(), description=fake.text(), price=random.uniform(20, 200))

    def populate_products(self):
        # Populate Product model with dummy data
        for _ in range(15):
            Product.objects.create(name=fake.word(), description=fake.text(), price=random.uniform(10, 100))

    def populate_employee_transactions(self):
        # Populate EmployeeTransaction model with dummy data
        for _ in range(20):
            EmployeeTransaction.objects.create(
                employee=random.choice(Employee.objects.all()),
                transaction_type=random.choice(['Salary', 'Bonus']),
                amount=random.uniform(500, 5000),
                date=fake.date_this_year(),
            )

    def populate_daily_summaries(self):
        # Populate DailySummary model with dummy data
        for _ in range(30):
            DailySummary.objects.create(
                date=fake.date_this_year(),
                total_sales=random.uniform(500, 5000),
                total_expenses=random.uniform(100, 1000),
                net_profit=None,  # Calculate this based on sales and expenses
            )

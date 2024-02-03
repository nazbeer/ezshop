from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _
from django.utils import timezone
from django.forms import inlineformset_factory

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=255)
#     date_of_birth = models.DateField(null=True, blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     phone_number = models.CharField(max_length=15, null=True, blank=True)

#     # Add more fields as needed

#     def __str__(self):
#         return self.username

# class CustomUserGroups(Group):
#     user_set = models.ManyToManyField(CustomUser, related_name='customuser_groups', blank=True, verbose_name=_('users'))
#     # Add any additional fields or methods for custom user groups

# class CustomUserPermissions(Permission):
#     user_set = models.ManyToManyField(CustomUser, related_name='customuser_permissions', blank=True, verbose_name=_('users'))
#     # Add any additional fields or methods for custom user permissions

class Module(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Shop(models.Model):
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    num_users = models.PositiveIntegerField()
    vat_remainder = models.BooleanField(default=False)
    employee_transaction_window = models.BooleanField(default=False)
    license_expiration_reminder = models.BooleanField(default=False)
    employee_visa_expiration_reminder = models.BooleanField(default=False)
    employee_passport_expiration_reminder = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ShopAdmin(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='admins')
    license_expiration = models.DateField()
    license_file = models.FileField(upload_to='license_files/')
    phone_number = models.CharField(max_length=20)
    vat_percentage = models.FloatField()
    vat_number = models.CharField(max_length=50)
    vat_submission_date = models.DateField()
    vat_certificate = models.FileField(upload_to='vat_certificates/')
    address = models.TextField()
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_expiration_reminder_days = models.PositiveIntegerField()
    vat_submission_date_reminder_days = models.PositiveIntegerField()
    employee_visa_expiration_reminder_days = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.shop.name} - {self.admin_user.username}"

class Role(models.Model):
    name = models.CharField(max_length=255)
    modules = models.ManyToManyField(Module)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    passport_no = models.CharField(max_length=20)
    passport_expiration_date = models.DateField()
    emirates_id = models.CharField(max_length=20)
    id_expiration_date = models.DateField()
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    house_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    transportation_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    joining_date = models.DateField()
    job_role = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.second_name}"

class ExpenseType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ReceiptType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class ReceiptTransaction(models.Model):
    date = models.DateField()
    receipt_type = models.ForeignKey(ReceiptType, on_delete=models.CASCADE)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()

class PaymentTransaction(models.Model):
    date = models.DateField()
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()

class BankDeposit(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  # Cash, Cheque, Bank Transfer
    narration = models.TextField()

class Service(models.Model):
    name = models.CharField(max_length=255)
    duration = models.DurationField()
    vat = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_allowed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    vat = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_allowed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class EmployeeTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('service', 'Service Transaction'),
        ('service_and_product', 'Service & Product Transaction'),
    ]

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    service_transactions = models.ManyToManyField(Service, related_name='service_transactions', blank=True)
    product_transactions = models.ManyToManyField(Product, related_name='product_transactions', blank=True)
    tip_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_option = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('card', 'Card')])

class DailySummary(models.Model):
    date = models.DateField()
    total_received_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_bank_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()

    def save(self, *args, **kwargs):
        # Calculate total_received_amount by summing employee transaction amounts
        total_received_amount = EmployeeTransaction.objects.filter(
            transaction_type='service_and_product'
        ).aggregate(models.Sum('total_amount'))['total_amount__sum'] or 0

        # Calculate total_expense_amount by summing payment transaction amounts
        total_expense_amount = PaymentTransaction.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0

        # Calculate total_bank_deposit by summing bank deposit amounts
        total_bank_deposit = BankDeposit.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0

        # Calculate balance
        balance = total_received_amount - total_expense_amount + total_bank_deposit

        self.total_received_amount = total_received_amount
        self.total_expense_amount = total_expense_amount
        self.total_bank_deposit = total_bank_deposit
        self.balance = balance

        super(DailySummary, self).save(*args, **kwargs)


class Sale(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    services = models.ManyToManyField(Service, through='SaleItem')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)


class SaleItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # You can add more fields as needed

    def __str__(self):
        return f"{self.service.name} - Quantity: {self.quantity}"


SaleItemFormSet = inlineformset_factory(Sale, SaleItem, fields=['product', 'quantity', 'price'])
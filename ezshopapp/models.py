from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django.utils import timezone
from django.forms import inlineformset_factory
from django.db.models import Sum
from datetime import timedelta
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD_CHOICES = (
    ("cash", "Cash"),
    ("card", "Card")
)


# class UserProfile(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='user_profiles')
#     email = models.EmailField(null=True)  # Nullable email field
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     created_on = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.username
    
class Modules(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_sidebar_choices(cls):

        sidebar_choices = [
            ('shop', 'Shop'),
            ('business', 'Business Profile'),
            ('employee', 'Employee'),
            ('sale', 'Sale & Day Closing'),
            ('role', 'Role'),
            ('expense-type', 'Expense Type'),
            ('receipt-transaction', 'Receipt Transaction'),
            ('payment-transaction', 'Payment Transaction'),
            ('service', 'Service'),
            ('product', 'Product'),
            ('employee-transaction', 'Employee Transaction'),
            ('daily-summary', 'Daily Summary'),
            ('bank', 'Bank Deposit'),
        ]
        return sidebar_choices

class Module(models.Model):
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255)
    modules = models.ManyToManyField(Module, default=None)
    is_employee = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

for choice in Modules.get_sidebar_choices():
    module_name = choice[1]
    Module.objects.get_or_create(name=module_name)
    

class Shop(models.Model):
    name = models.CharField(max_length=255, verbose_name='Shop Name')
    license_number = models.CharField(max_length=50, unique=True)
    num_users = models.PositiveIntegerField(verbose_name='Number of Users')
    vat_remainder = models.BooleanField(default=False, verbose_name='VAT Reminder')
    employee_transaction_window = models.BooleanField(default=False)
    license_expiration_reminder = models.BooleanField(default=False, verbose_name='License Expiration Reminder')
    employee_visa_expiration_reminder = models.BooleanField(default=False, verbose_name='Employee Visa Expiration Reminder')
    employee_passport_expiration_reminder = models.BooleanField(default=False, verbose_name='Employee Passport Expiration Reminder')
    admin_email = models.EmailField(max_length=100, default='')
    
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class ShopAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, verbose_name="Mite Admin User")
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    #admin_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_admin', unique=True)
    
    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "No User Assigned"



class BusinessProfile(models.Model):
    name = models.CharField(max_length=64, blank=False, default=None, null=True)
    license_number = models.CharField(max_length=255)
    license_expiration = models.DateField(null=True)
    license_upload = models.FileField(upload_to='licenses')
    shop_phone_number = models.CharField(max_length=25)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    vat_number = models.CharField(max_length=255)
    vat_submission_date_1 = models.DateField(null=True)
    vat_submission_date_2 = models.DateField(null=True)
    vat_submission_date_3 = models.DateField(null=True)
    vat_certificate_upload = models.FileField(upload_to='vat_certificates')
    address = models.TextField()
    license_expiration_reminder_days = models.PositiveIntegerField(verbose_name='License Expiration Reminder (days)')
    vat_submission_date_reminder_days = models.PositiveIntegerField(verbose_name='VAT Submission Date Reminder (days)')
    employee_visa_expiration_reminder_days = models.PositiveIntegerField(verbose_name='Employee Visa Expiration Reminder (days)')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    business_profile = models.ForeignKey('BusinessProfile', on_delete=models.CASCADE)
    email = models.EmailField()
    mobile = models.CharField(max_length=25, null=True)
    password = models.CharField(max_length=128, default='ezshop@2024')  
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):

        if not self.user.username:
            self.user.username = self.email  
        if not self.user.password:
            self.user.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email 

class ExpenseType(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class ReceiptType(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class ReceiptTransaction(models.Model):
    date = models.DateField()
    receipt_type = models.ForeignKey(ReceiptType, on_delete=models.CASCADE)
    received_amount = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)

class PaymentTransaction(models.Model):
    date = models.DateField()
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)

class BankDeposit(models.Model):
    date = models.DateField()
    deposit_date = models.DateField(null=True, blank=True)  # Old field for deposit date
    #new_deposit_date = models.DateField(null=True, blank=True)  # New field for deposit date
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  
    narration = models.TextField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Bank model
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Bank Deposit on {self.date}"
    
class Service(models.Model):
    name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField() 
    vat = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_allowed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    vat = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_allowed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    business_profile = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    passport_no = models.CharField(max_length=20)
    passport_expiration_date = models.DateField()
    emirates_id = models.CharField(max_length=20)
    id_expiration_date = models.DateField()
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    house_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    transportation_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    joining_date = models.DateField()
    job_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    is_employee = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.second_name}"
    
    

class EmployeeTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('service', 'Service Transaction'),
        ('product', 'Product Transaction'),
        ('service_and_product', 'Service & Product Transaction'),
    ]

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    service_transactions = models.ManyToManyField(Service, related_name='service_transactions', blank=True)
    product_transactions = models.ManyToManyField(Product, related_name='product_transactions', blank=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_option = models.CharField(max_length=10, choices=[('cash', 'Cash'), ('card', 'Card')])
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    #day_closing = models.ForeignKey(DayClosing, on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"Employee Transaction - {self.id}"

class DayClosing(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(EmployeeTransaction, on_delete=models.CASCADE, blank=True, null=True)  
    total_services = models.DecimalField(max_digits=8, decimal_places=2)
    total_sales = models.DecimalField(max_digits=8, decimal_places=2)
    total_collection = models.DecimalField(max_digits=8, decimal_places=2)
    advance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    net_collection = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    
    @classmethod
    def calculate_totals(cls):
        date = timezone.now().date()  
        total_services = SalesByStaffItemService.objects.filter(date=date).count()
        total_sales = SalesByStaffItemService.objects.filter(date=date).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        return {
            'total_services': total_services,
            'total_sales': total_sales,
        }
    

class DayClosingAdmin(models.Model):
    date = models.DateField(default=timezone.now)
    total_services = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_collection = models.DecimalField(max_digits=10, decimal_places=2)
    advance = models.DecimalField(max_digits=10, decimal_places=2)
    net_collection = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    # @classmethod
    # def calculate_totals(cls):
    #     date = timezone.now().date()  
    #     total_services = SaleByAdminService.objects.filter(date=date).count()
    #     total_sales = SaleByAdminService.objects.filter(date=date).aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    #     return {
    #         'total_services': total_services,
    #         'total_sales': total_sales,
    #     }
class DailySummary(models.Model):
    date = models.DateField()
    total_received_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_bank_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):

        total_received_amount = EmployeeTransaction.objects.filter(
            transaction_type='service_and_product'
        ).aggregate(models.Sum('total_amount'))['total_amount__sum']

        total_expense_amount = PaymentTransaction.objects.aggregate(models.Sum('amount'))['amount__sum'] 

        total_bank_deposit = BankDeposit.objects.aggregate(models.Sum('amount'))['amount__sum'] 

        balance = total_received_amount - total_expense_amount + total_bank_deposit

        self.total_received_amount = total_received_amount
        self.total_expense_amount = total_expense_amount
        self.total_bank_deposit = total_bank_deposit
        self.balance = balance

        super(DailySummary, self).save(*args, **kwargs)
        self.created_on = timezone.now()

class Sale(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    services = models.ManyToManyField(Service, through='SaleItem')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

class SaleItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

SaleItemFormSet = inlineformset_factory(Sale, SaleItem, fields=['product', 'quantity', 'price'])

class SaleByAdminService(models.Model):
    date = models.DateField(null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    payment_method = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def total_amount(self):
        return (self.price * self.quantity) - self.discount + self.tip

class SalesByAdminItem(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.date)

class SalesByStaffItemService(models.Model):
    date = models.DateField(_("Date"))
    #eid=models.CharField(max_length=50, null=True)
    #employee = models.CharField(max_length=50,  null=True, verbose_name=_("Employee"))
    #employee_id = models.IntegerField(default='1', verbose_name=_("Employee ID"), null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"),  null=True)
    pquantity = models.PositiveIntegerField(_("Product Quantity"),  null=True)
    pprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Product Price"),  null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_("Service"),  null=True)
    squantity = models.PositiveIntegerField(_("Service Quantity"),  null=True)
    sprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Service Price"),  null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Sub Total"))
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Discount"), null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"), null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Payment Method"))
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Sale on {self.date}"
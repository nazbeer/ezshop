from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import pre_save
import pytz

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD_CHOICES = (
    ("cash", "Cash"),
    ("card", "Card")
)

class Modules(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_sidebar_choices(cls):

        sidebar_choices = [
            ('/sale/dayclosing/',  'Day Closing'),
            ('/dayclosing/admin/ ',  'Admin Day Closing'),
            ('/sale/sales-by-staff-item-service/', 'Sales by Staff - Product/Service'),
            ('/sale/sales-by-staff-service/', 'Sales by Staff - Service'),
            ('/sale/sales-by-staff-item/', 'Sales by Staff - Product'),
            ('/sale/day-closing-report/',  'Day Closing Report'),
            ('/sale/sales-report/',  'Sales Report'),
        ]
        return sidebar_choices
class Module(models.Model):
    URL_CHOICES = [
        ('/sale/dayclosing/', 'Day Closing'),
        ('/dayclosing/admin/', 'Admin Day Closing'),
        ('/sale/sales-by-staff-item-service/', 'Sales by Staff - Product/Service'),
        ('/sale/sales-by-staff-service/', 'Sales by Staff - Service'),
        ('/sale/sales-by-staff-item/', 'Sales by Staff - Product'),
        ('/sale/day-closing-report/', 'Day Closing Report'),
        ('/sale/sales-report/', 'Sales Report'),
    ]
    URL_NAMES = [
        ('Day Closing', '/sale/dayclosing/'),
        ('Admin Day Closing', '/dayclosing/admin/'),
        ('Sales by Staff - Product/Service', '/sale/sales-by-staff-item-service/'),
        ('Sales by Staff - Service', '/sale/sales-by-staff-service/'),
        ('Sales by Staff - Product', '/sale/sales-by-staff-item/'),
        ('Day Closing Report', '/sale/day-closing-report/'),
        ('Sales Report', '/sale/sales-report/'),
    ]
    url = models.CharField(max_length=150, choices=URL_CHOICES, null=True, verbose_name='Page Name')
    name = models.CharField(max_length=50, choices=URL_NAMES, null=True, verbose_name='Page URL')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name



class Shop(models.Model):
    name = models.CharField(max_length=255, verbose_name='Shop Name')
    license_number = models.CharField(max_length=50, unique=True)
    num_users = models.PositiveIntegerField(verbose_name='Number of Users')
    vat_remainder = models.BooleanField(default=True, verbose_name='VAT Reminder')
    employee_transaction_window = models.BooleanField(default=True)
    license_expiration_reminder = models.BooleanField(default=True, verbose_name='License Expiration Reminder')
    employee_visa_expiration_reminder = models.BooleanField(default=True, verbose_name='Employee Visa Expiration Reminder')
    employee_passport_expiration_reminder = models.BooleanField(default=True, verbose_name='Employee Passport Expiration Reminder')
    admin_email = models.EmailField(max_length=100, default='')
    
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    
class ShopAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, verbose_name="Mite Admin User")
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)
    
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
    
    def license_expiration_reminder_due(self):
        return (self.license_expiration - timezone.now().date()).days <= self.license_expiration_reminder_days

    def vat_submission_date_reminder_due(self):
        today = timezone.now().date()
        return (
            (self.vat_submission_date_1 and (self.vat_submission_date_1 - today).days <= self.vat_submission_date_reminder_days) or
            (self.vat_submission_date_2 and (self.vat_submission_date_2 - today).days <= self.vat_submission_date_reminder_days) or
            (self.vat_submission_date_3 and (self.vat_submission_date_3 - today).days <= self.vat_submission_date_reminder_days)
        )

class Role(models.Model):
    name = models.CharField(max_length=255)
    modules = models.ManyToManyField(Module, default=None)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, default=None, null=True)
    is_employee = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

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
    deposit_date = models.DateField(null=True, blank=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  
    narration = models.TextField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)
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
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    vat = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_allowed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    business_profile = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    business_profile = models.CharField(max_length=255, null=True)
    business_profile_id = models.IntegerField(null=True)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    passport_no = models.CharField(max_length=20, unique=True)
    passport_expiration_date = models.DateField()
    emirates_id = models.CharField(max_length=20, unique=True)
    id_expiration_date = models.DateField()
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    house_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transportation_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    joining_date = models.DateField()
    job_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    is_employee = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.second_name}"
    
    def id_expiration_due(self):
        business_profile = BusinessProfile.objects.get(id=self.business_profile_id)
        reminder_days = business_profile.employee_visa_expiration_reminder_days
        expiration_due_date = self.id_expiration_date - timedelta(days=reminder_days)
        return expiration_due_date <= timezone.now().date()

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
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"Employee Transaction - {self.id}"

class DayClosing(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)  
    total_services = models.DecimalField(max_digits=8, decimal_places=2)
    total_sales = models.DecimalField(max_digits=8, decimal_places=2)
    total_collection = models.DecimalField(max_digits=8, decimal_places=2)
    advance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    net_collection = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Day Closing by {self.employee.first_name} on {self.date}"

class DayClosingAdmin(models.Model):
    date = models.DateField(default=timezone.now)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)  
    total_services = models.PositiveIntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_collection = models.DecimalField(max_digits=10, decimal_places=2)
    advance = models.DecimalField(max_digits=10, decimal_places=2)
    net_collection = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

class DailySummary(models.Model):
    date = models.DateField()
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_received_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_bank_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Daily Summary on {self.date}"

class Sale(models.Model):
    date = models.DateField()
    services = models.ManyToManyField(Service)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

class SaleByStaffService(models.Model):
    date = models.DateField(_("Date"))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("Employee"), null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"), null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.date)
    
class SaleByStaffItem(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("Employee"), null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"), null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Sale on {self.date}"  
  
class SaleByAdminService(models.Model):
    date = models.DateField(_("Date"), null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("Employee"), null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_("Service"),  null=True)
    quantity = models.PositiveIntegerField(_("Service Quantity"),  null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Service Price"),  null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Payment Method"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"), null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Sale on {self.date}"
    
class SalesByAdminItem(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("Employee"), null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"), null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Sale on {self.date}"
class SalesByStaffItemService(models.Model):
    date = models.DateField(_("Date"))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("Employee"), null=True)
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
    itemtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Products Total"), null=True)
    servicetotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Service Total"), null=True)
    
    def __str__(self):
        return f"Sale on {self.date}"

@receiver(pre_save)
def set_created_on_timezone(sender, instance, **kwargs):
    if hasattr(instance, 'created_on') and not instance.created_on:
        dubai_timezone = pytz.timezone('Asia/Dubai')
        instance.created_on = timezone.localtime(timezone.now(), dubai_timezone)

pre_save.connect(set_created_on_timezone)
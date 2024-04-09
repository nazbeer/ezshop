from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.site_header = "Ezshop Admin"
admin.site.site_title = "Ezshop Admin Portal"
admin.site.index_title = "Welcome to Ezshop Mite Solution App"

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'shop'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CustomShopAdminAdmin(admin.ModelAdmin):
    list_display = ('get_shop_name', 'get_admin_username')
    search_fields = ['shop__name', 'admin_user__username']

    def get_shop_name(self, obj):
        return obj.shop.name

    def get_admin_username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return "No User Assigned"

    get_shop_name.short_description = 'Shop Name'
    get_admin_username.short_description = 'Admin Username'

admin.site.register(ShopAdmin, CustomShopAdminAdmin)
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_number', 'num_users', 'vat_remainder', 'employee_transaction_window', 'license_expiration_reminder', 'employee_visa_expiration_reminder', 'employee_passport_expiration_reminder', 'admin_email', 'created_on']


# @admin.register(Modules)
# class ModulesAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_on']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on']


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_number', 'license_expiration', 'shop_phone_number', 'vat_percentage', 'vat_number', 'vat_submission_date_1', 'vat_submission_date_2', 'vat_submission_date_3', 'address', 'license_expiration_reminder_days', 'vat_submission_date_reminder_days', 'employee_visa_expiration_reminder_days', 'created_on', 'license_expiration_reminder_due', 'vat_submission_date_reminder_due']

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_profile', 'is_employee', 'created_on']

@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on']

@admin.register(ReceiptType)
class ReceiptTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_on']

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_number', 'opening_balance', 'created_on']

@admin.register(ReceiptTransaction)
class ReceiptTransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'receipt_type', 'received_amount', 'narration', 'created_on']

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'expense_type', 'amount', 'narration', 'created_on']

@admin.register(BankDeposit)
class BankDepositAdmin(admin.ModelAdmin):
    list_display = ['date', 'deposit_date', 'amount', 'transaction_type', 'narration', 'bank', 'created_on']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'username', 'password', 'business_profile', 'business_profile_id', 'first_name', 'second_name', 'nationality', 'mobile_no', 'passport_no', 'passport_expiration_date', 'emirates_id', 'id_expiration_date', 'basic_pay', 'house_allowance', 'transportation_allowance', 'commission_percentage', 'joining_date', 'job_role', 'is_employee', 'created_on', 'id_expiration_due']

# @admin.register(EmployeeTransaction)
# class EmployeeTransactionAdmin(admin.ModelAdmin):
#     list_display = ['transaction_type', 'total_amount', 'payment_option', 'employee', 'created_on']

# @admin.register(DayClosing)
# class DayClosing(admin.ModelAdmin):
#     list_display = ['date', 'employee', 'total_services', 'total_sales', 'total_collection', 'advance', 'net_collection', 'status', 'created_on']

@admin.register(DayClosingAdmin)
class DayClosingAdminAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'total_services', 'total_sales', 'total_collection', 'advance', 'net_collection', 'status', 'created_on']

@admin.register(DailySummary)
class DailySummaryAdmin(admin.ModelAdmin):
    list_display = ['date', 'opening_balance', 'total_received_amount', 'total_expense_amount', 'total_bank_deposit', 'balance', 'narration', 'created_on']

# @admin.register(Sale)
# class SaleAdmin(admin.ModelAdmin):
#     list_display = ['date', 'amount', 'discount', 'net_amount', 'created_on']

@admin.register(SaleByStaffService)
class SaleByStaffServiceAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'service', 'quantity', 'price', 'total_amount', 'payment_method', 'created_on']

@admin.register(SaleByStaffItem)
class SaleByStaffItemAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'item', 'quantity', 'price', 'total_amount', 'payment_method', 'created_on']

@admin.register(SaleByAdminService)
class SaleByAdminServiceAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'service', 'quantity', 'price', 'total_amount', 'payment_method', 'created_on']

@admin.register(SalesByAdminItem)
class SalesByAdminItemAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'item', 'quantity', 'price', 'total_amount', 'payment_method', 'created_on']

@admin.register(SalesByStaffItemService)
class SalesByStaffItemServiceAdmin(admin.ModelAdmin):
    list_display = ['date', 'employee', 'product', 'pquantity', 'pprice', 'service', 'squantity', 'sprice', 'sub_total', 'discount', 'total_amount', 'payment_method', 'created_on', 'itemtotal', 'servicetotal']


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['name', 'vat','amount','max_discount_allowed','status','business_profile','created_on']

@admin.register(Service)
class Service(admin.ModelAdmin):
    list_display = ['name','duration', 'vat','amount','max_discount_allowed','status','business_profile','created_on']

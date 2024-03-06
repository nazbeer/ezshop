from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
    Shop, Sale, DayClosing, Employee, UserProfile, AdminProfile,
    Service, BusinessProfile, SalesByAdminItem, SaleByAdminService,
    Role, SaleItem, ExpenseType, ReceiptType, Bank, ReceiptTransaction,
    PaymentTransaction, BankDeposit, Product, EmployeeTransaction,
    DailySummary, SalesByStaffItemService, DayClosingAdmin, ShopAdmin
)

admin.site.site_header = "Ezshop Admin"
admin.site.site_title = "Ezshop Admin Portal"
admin.site.index_title = "Welcome to Ezshop Mite Solution App"

class ShopAdminModel(admin.ModelAdmin):
    list_display = ('name', 'username','email', 'license_number', 'num_users', 'created_on')  # Adjust list_display according to your model fields
    search_fields = ['name', 'license_number', 'location']  # Adjust search_fields according to your model fields
    list_filter = ['created_on']  # Adjust list_filter according to your model fields

# Register the Shop model with the custom admin class
admin.site.register(Shop, ShopAdminModel)

# Extend the UserAdmin to include Shop details inline
class ShopInline(admin.StackedInline):
    model = ShopAdmin
    can_delete = False
    verbose_name_plural = 'admins'

# Extend the UserAdmin to include Shop details
class CustomUserAdmin(UserAdmin):
    inlines = (ShopInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(ShopAdmin)

# Register other models
admin.site.register(Sale)
admin.site.register(Employee)
admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(BusinessProfile)
admin.site.register(DayClosing)
admin.site.register(DayClosingAdmin)
admin.site.register(SaleByAdminService)
admin.site.register(Role)
admin.site.register(SaleItem)
admin.site.register(ExpenseType)
admin.site.register(ReceiptType)
admin.site.register(Bank)
admin.site.register(ReceiptTransaction)
admin.site.register(PaymentTransaction)
admin.site.register(BankDeposit)
admin.site.register(Product)
admin.site.register(EmployeeTransaction)
admin.site.register(DailySummary)
admin.site.register(SalesByAdminItem)
admin.site.register(SalesByStaffItemService)

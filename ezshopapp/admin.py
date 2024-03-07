from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *

admin.site.site_header = "Ezshop Admin"
admin.site.site_title = "Ezshop Admin Portal"
admin.site.index_title = "Welcome to Ezshop Mite Solution App"


admin.site.register(Shop)
# class Shop(admin.ModelAdmin):
#     list_display = ('shop', 'license_number')
#     search_fields = ['shop__name', 'email']
#     list_filter = ['shop']
   
class ShopAdminAdmin(admin.ModelAdmin):
    list_display = ('shop', 'email')
    search_fields = ['shop__name', 'email', 'admin_user__username']
    list_filter = ['shop']
    raw_id_fields = ['admin_user']
    #max_num = 1 
    # def get_admin_users(self, obj):
    #     return ", ".join([admin.user.username for admin in obj.admin_user.all()])
    # get_admin_users.short_description = 'Admin Users'

admin.site.register(ShopAdmin, ShopAdminAdmin)

class ShopInline(admin.StackedInline):
    model = ShopAdmin
    can_delete = False
    verbose_name_plural = 'Shop Admins'
    max_num = 1 
    
class CustomUserAdmin(UserAdmin):
    inlines = (ShopInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

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

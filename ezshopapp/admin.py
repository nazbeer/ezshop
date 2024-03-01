from django.contrib import admin
from .models import Shop, ShopAdmin, Sale, Employee, UserProfile, AdminProfile, Service, BusinessProfile, DayClosing, SalesByAdminItem, SaleByAdminService, Role, SaleItem, ExpenseType, ReceiptType, Bank, ReceiptTransaction, PaymentTransaction, BankDeposit, Product, EmployeeTransaction, DailySummary, SalesByAdminItem, SalesByStaffItemService

admin.site.site_header = "Ezshop Admin"
admin.site.site_title = "Ezshop Admin Portal"
admin.site.index_title = "Welcome to Ezshop Mite Solution App"

admin.site.register(Shop)
admin.site.register(ShopAdmin)
admin.site.register(Sale)
admin.site.register(Employee)
admin.site.register(UserProfile)
admin.site.register(AdminProfile)
admin.site.register(Service)
admin.site.register(BusinessProfile)
admin.site.register(DayClosing)

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

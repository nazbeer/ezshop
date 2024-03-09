from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from django import forms
admin.site.site_header = "Ezshop Admin"
admin.site.site_title = "Ezshop Admin Portal"
admin.site.index_title = "Welcome to Ezshop Mite Solution App"


# class CustomUserAdmin(BaseUserAdmin):
#     add_form = CustomUserCreationForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'shop'),
#         }),
#     )

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'shop'),
        }),
    )
    # list_display = ('username', 'email',)  # Add 'get_shop' to list_display
    # search_fields = ['username', 'email']

    # def get_shop(self, obj):
    #     return obj.shop.name if obj.shop else None  # Return shop name if exists, else None

    # get_shop.short_description = 'Shop'  # Set the column header name


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

# class CustomShopAdminAdmin(admin.ModelAdmin):
#     form = CustomShopAdminForm
#     list_display = ('name', 'admin_email')
#     search_fields = ['shop__name', 'admin_user__email']
#     list_filter = ['name']  # Update list_filter to use the 'name' field instead of 'shop'


#     def shop_name(self, obj):
#         return obj.shop.name

#     def admin_email(self, obj):
#         return obj.admin_user.email

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(admin_user=request.user)

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         existing_shop_count = ShopAdmin.objects.filter(admin_user=instance.admin_user).count()
#         if existing_shop_count >= 1:
#             self.message_user(
#                 self.request,
#                 "Only one shop can be created under each user.",
#                 level=admin.messages.ERROR
#             )
#             return super().form_invalid(form)
#         else:
#             return super().form_valid(form)

#     shop_name.short_description = 'Shop Name'
#     admin_email.short_description = 'Admin Email'




# class CustomUserAdmin(UserAdmin):
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         existing_shop_count = ShopAdmin.objects.filter(admin_user=user).count()
#         if existing_shop_count >= 1:
#             self.message_user(
#                 self.request,
#                 "Only one shop can be created under each user.",
#                 level=admin.messages.ERROR
#             )
#             return super().form_invalid(form)
#         else:
#             return super().form_valid(form)

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Shop, CustomShopAdminAdmin)


# class ShopAdminInline(admin.StackedInline):
#     model = ShopAdmin
#     can_delete = False
#     max_num = 1
#     fk_name = 'admin_user'
# class ShopAdminAdmin(admin.ModelAdmin):
#     model = ShopAdmin
#     list_display = ['shop', ]  # Replace 'user' with the correct field
#     search_fields = ['admin_user__username', 'shop__name']
#     list_filter = ['shop']

# class ShopAdminUserAdmin(BaseUserAdmin):
#     inlines = [ShopAdminInline]

# # Unregister the default UserAdmin
# admin.site.unregister(User)
# # Register User with the custom ShopAdminUserAdmin
# admin.site.register(User, ShopAdminUserAdmin)

# admin.site.register(Shop, ShopAdminAdmin)
admin.site.register(Shop)
#admin.site.register(ShopAdmin)
admin.site.register(Sale)
admin.site.register(Employee)
#admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(BusinessProfile)
# admin.site.register(DayClosing)
# admin.site.register(DayClosingAdmin)
admin.site.register(SaleByAdminService)
# admin.site.register(Role)
# admin.site.register(SaleItem)
# admin.site.register(ExpenseType)
# admin.site.register(ReceiptType)
admin.site.register(Bank)
# admin.site.register(ReceiptTransaction)
# admin.site.register(PaymentTransaction)
# admin.site.register(BankDeposit)
# admin.site.register(Product)
# admin.site.register(EmployeeTransaction)
# admin.site.register(DailySummary)
# admin.site.register(SalesByAdminItem)
admin.site.register(SalesByStaffItemService)

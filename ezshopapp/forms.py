from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.db import models
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2', 'full_name', 'date_of_birth', 'profile_picture', 'address', 'phone_number')
class CustomUserCreationForm(UserCreationForm):
    shop = forms.ModelChoiceField(queryset=Shop.objects.all())

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('shop', )

    def clean(self):
        cleaned_data = super().clean()
        shop = cleaned_data.get('shop')
        username = cleaned_data.get('username')

        if shop:
            # Check if the shop is already associated with another admin user
            try:
                existing_shop_admin = ShopAdmin.objects.get(shop=shop)
                raise forms.ValidationError(f"This shop is already associated with the user {existing_shop_admin.admin_user.username}")
            except ShopAdmin.DoesNotExist:
                pass

            # Check if the shop is already associated with the username
            try:
                existing_user = User.objects.get(username=username)
                existing_shop_admin = ShopAdmin.objects.get(admin_user=existing_user)
                if existing_shop_admin.shop == shop:
                    raise forms.ValidationError(f"This shop is already associated with your username")
            except User.DoesNotExist:
                pass

        if ShopAdmin.objects.filter(shop=shop).exists():
            raise forms.ValidationError("This shop is already associated with a user.")
        
        return cleaned_data
    
class CustomShopAdminForm(forms.ModelForm):
    class Meta:
        model = ShopAdmin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing_shops = ShopAdmin.objects.values_list('shop_id', flat=True)
        self.fields['name'].queryset = Shop.objects.exclude(id__in=existing_shops)


# class AdminUserForm(forms.Form):
#     username = forms.CharField(max_length=150)
#     password = forms.CharField(widget=forms.PasswordInput)
    
# class AdminProfileForm(forms.ModelForm):
#     class Meta:
#         model = AdminProfile
#         fields = ['email', 'mobile', 'password']

    # username = forms.CharField(max_length=150, required=False)  # Add username field

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     #self.fields['employee'].queryset = EmployeeForm.objects.all()  # Assuming Employee model is defined

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if not username:
    #         # Use email as username if not provided
    #         username = self.cleaned_data['email']
    #     return username
    

class ShopAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'

class BusinessProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Get the user from the form kwargs
        user = kwargs.pop('user', None)
        super(BusinessProfileForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            # Filter shop choices based on the currently logged-in user's associated shop
            self.fields['shop'].queryset = Shop.objects.filter(admin_user=user)

    class Meta:
        model = BusinessProfile
        fields = '__all__'

 
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'

class DayClosingFormAdmin(forms.ModelForm):
    class Meta:
        model = DayClosingAdmin
        #fields = ['total_collection', 'advance', 'net_collection', 'employee']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        employee_id = cleaned_data.get('employee_id')
        passport_no = cleaned_data.get('passport_no')
        emirates_id = cleaned_data.get('emirates_id')
        business_profile_id = cleaned_data.get('business_profile_id')
        print(business_profile_id)
        if Employee.objects.exclude(pk=self.instance.pk).filter( business_profile_id=business_profile_id,employee_id=employee_id).exists():
            self.add_error('employee_id', 'Employee ID must be unique.')
        if Employee.objects.exclude(pk=self.instance.pk).filter(business_profile_id=business_profile_id,passport_no=passport_no).exists():
            self.add_error('passport_no', 'Passport No must be unique.')
        if Employee.objects.exclude(pk=self.instance.pk).filter(business_profile_id=business_profile_id,emirates_id=emirates_id).exists():
            self.add_error('emirates_id', 'Emirates ID must be unique.')
            

class EmployeeLoginForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['username', 'password', 'is_employee']
        widgets = {
            'password': forms.PasswordInput(),
        }

class DayClosingForm(forms.ModelForm):
    class Meta:
        model = DayClosing
        fields = ['date', 'employee', 'total_services', 'total_sales', 'total_collection', 'advance', 'net_collection', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class DayClosingAdminForm(forms.ModelForm):
    class Meta:
        model = DayClosingAdmin
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'total_collection': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'advance': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'net_collection': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'required': 'required'}),
        }

class ExpenseTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = '__all__'

class ReceiptTypeForm(forms.ModelForm):
    class Meta:
        model = ReceiptType
        fields = ['name']

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'


class ReceiptTransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super(ReceiptTransactionForm, self).__init__(*args, **kwargs)
        if business_profile:
            self.fields['receipt_type'].queryset = ReceiptType.objects.filter(business_profile = business_profile)

    class Meta:
        model = ReceiptTransaction
        fields = ['date', 'receipt_type', 'business_profile', 'received_amount', 'narration']

class PaymentTransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super(PaymentTransactionForm, self).__init__(*args, **kwargs)
        if business_profile:
            self.fields['expense_type'].queryset = ExpenseType.objects.filter(business_profile = business_profile)

    # def __init__(self, *args, **kwargs):
    #     """ Grants access to the request object so that only members of the current user
    #     are given as options"""

    #     self.request = kwargs.pop('request')
    #     super(PaymentTransactionForm, self).__init__(*args, **kwargs)
    #     shop_admin = ShopAdmin.objects.get(user=self.request.user)
    #     shop = shop_admin.shop
    #     self.business_profile = BusinessProfile.objects.get(name=shop.name)
    #     self.fields['expense_type'].queryset = ExpenseType.objects.filter(
    #         business_profile=self.business_profile.id)

    class Meta:
        model = PaymentTransaction
        fields = '__all__'




class BankDepositForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        business_profile = kwargs.pop('business_profile', None)
        super(BankDepositForm, self).__init__(*args, **kwargs)
        if business_profile:
            self.fields['bank'].queryset = Bank.objects.filter(business_profile = business_profile)
    
    class Meta:
        model = BankDeposit
        fields = ['date','deposit_date','amount','transaction_type','narration','bank','business_profile']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class EmployeeTransactionForm(forms.ModelForm):
    class Meta:
        model = EmployeeTransaction
        fields = '__all__'

class DailySummaryForm(forms.ModelForm):
    class Meta:
        model = DailySummary
        fields = ['date','opening_balance','total_received_amount','total_expense_amount','total_bank_deposit','balance','narration','business_profile','advance']
        widgets = {
                'date': forms.DateInput(attrs={'type': 'date'}),
            }

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
# class SalesForm(forms.ModelForm):
#     class Meta:
#         model = Sale
#         fields = '__all__'


# class SaleItemForm(forms.ModelForm):
#     class Meta:
#         model = SaleItem
#         fields = ['service', 'quantity']

# class SalesbyAdminItemForm(forms.ModelForm):
#     class Meta:
#         model = SalesbyAdminItem
#         fields = ['date', 'employee', 'payment_method']

# class SalesbyAdminItemSaleItemForm(forms.ModelForm):
#     class Meta:
#         model = SalesbyAdminItemSaleItem
#         fields = ['item', 'quantity']

# SalesbyAdminItemFormSet = forms.inlineformset_factory(
#     SalesbyAdminItem, SalesbyAdminItemSaleItem, form=SalesbyAdminItemSaleItemForm, extra=1, can_delete=True
# )

# SaleItemFormSet = inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=1, can_delete=True)


class SalesByStaffServiceForm(forms.ModelForm):
    class Meta:
        model = SaleByStaffService
        fields = '__all__'

class SaleByAdminServiceForm(forms.ModelForm):
    class Meta:
        model = SaleByAdminService
        fields = '__all__'
        

class SaleByStaffItemForm(forms.ModelForm):
    class Meta:
        model = SaleByStaffItem
        fields = '__all__'

class SalesByAdminItemForm(forms.ModelForm):
    class Meta:
        model = SalesByAdminItem
        fields = '__all__'
        #fields = ['date', 'employee', 'item', 'quantity', 'price', 'discount', 'payment_method']

class SalesByStaffItemServiceForm(forms.ModelForm):
    class Meta:
        model = SalesByStaffItemService
        fields = '__all__'


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_style', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form_style', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form_style', 'placeholder': 'Message', 'rows': 3}),
        }

from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import Shop, Sale,Employee, AdminProfile, Service,BusinessProfile,DayClosing,  SalesByAdminItem, SaleByAdminService, Role, SaleItem, Employee, ExpenseType, ReceiptType, Bank, ReceiptTransaction, PaymentTransaction, BankDeposit, Service, Product, EmployeeTransaction, DailySummary, SalesByAdminItem,SalesByStaffItemService
from django.db import models
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2', 'full_name', 'date_of_birth', 'profile_picture', 'address', 'phone_number')
    

class AdminUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['email', 'mobile', 'password']

    username = forms.CharField(max_length=150, required=False)  # Add username field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['employee'].queryset = EmployeeForm.objects.all()  # Assuming Employee model is defined

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            # Use email as username if not provided
            username = self.cleaned_data['email']
        return username
    
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'
class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        exclude = ['admins']  # Exclude admins field as it will be handled separately

    # def clean_vat_certificate_upload(self):
    #     data = self.cleaned_data['vat_certificate_upload']
    #     if data:
    #         if not data.name.endswith('.pdf, .png, .jpg, .jpeg'):
    #             raise ValidationError('Only PDF files are allowed.')
    #     return data
    
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'passport_expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'id_expiration_date': forms.DateInput(attrs={'type': 'date'}),
             'password': forms.PasswordInput(),
             'joining_date': forms.DateInput(attrs={'type': 'date'}),
            # Add more widgets for other date fields if needed
        }

class DayClosingForm(forms.ModelForm):
    class Meta:
        model = DayClosing
        fields = '__all__' 

class ExpenseTypeForm(forms.ModelForm):
    class Meta:
        model = ExpenseType
        fields = '__all__'

class ReceiptTypeForm(forms.ModelForm):
    class Meta:
        model = ReceiptType
        fields = '__all__'

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'

class ReceiptTransactionForm(forms.ModelForm):
    class Meta:
        model = ReceiptTransaction
        fields = '__all__'

class PaymentTransactionForm(forms.ModelForm):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'

class BankDepositForm(forms.ModelForm):
    class Meta:
        model = BankDeposit
        fields = '__all__'

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
        fields = '__all__'


class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
class SalesForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['amount', 'discount', 'tip']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].required = True
        self.services = kwargs.pop('services', None)
        self.fields['amount'].initial = self.calculate_total_amount()
    
    def calculate_total_amount(self):
        total_amount = 0
        if self.services:
            for service in self.services:
                total_amount += service.price * service.quantity

        # Apply discount
        discount = self.cleaned_data.get('discount', 0)
        total_amount -= discount

        return total_amount

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'employee', 'amount', 'discount', 'tip', 'net_amount']

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['service', 'quantity']

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

SaleItemFormSet = inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=1, can_delete=True)


class SaleByAdminServiceForm(forms.ModelForm):
    class Meta:
        model = SaleByAdminService
        fields = '__all__'
        #fields = ['date', 'employee', 'service', 'quantity', 'price', 'discount', 'tip', 'payment_method']


class SalesByAdminItemForm(forms.ModelForm):
    class Meta:
        model = SalesByAdminItem
        fields = '__all__'
        #fields = ['date', 'employee', 'item', 'quantity', 'price', 'discount', 'payment_method']


class SalesByStaffItemServiceForm(forms.ModelForm):
    class Meta:
        model = SalesByStaffItemService
        fields = ['date', 'product', 'pquantity', 'pprice', 'service', 'squantity', 'sprice', 'sub_total', 'discount', 'total_amount', 'payment_method']
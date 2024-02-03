from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import Shop, Sale, Service, SaleItem, Role, Employee, ExpenseType, ReceiptType, Bank, ReceiptTransaction, PaymentTransaction, BankDeposit, Service, Product, EmployeeTransaction, DailySummary
from django.db import models
from django.forms import inlineformset_factory


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2', 'full_name', 'date_of_birth', 'profile_picture', 'address', 'phone_number')
    
class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
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



class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'employee', 'amount', 'discount', 'tip', 'net_amount']

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['service', 'quantity']

SaleItemFormSet = inlineformset_factory(Sale, SaleItem, form=SaleItemForm, extra=1, can_delete=True)
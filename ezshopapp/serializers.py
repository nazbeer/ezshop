from rest_framework import serializers
from .models import *

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class ShopAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAdmin
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = '__all__'

class ReceiptTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptType
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class ReceiptTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptTransaction
        fields = '__all__'

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'

class BankDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDeposit
        fields = '__all__'



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class EmployeeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTransaction
        fields = '__all__'

class DailySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySummary
        fields = '__all__'

# class SaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sale
#         fields = '__all__'



class SalesByStaffItemServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesByStaffItemService
        fields = '__all__'


class SaleByStaffServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleByStaffService
        fields = '__all__'


class SalesByStaffItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleByStaffItem
        fields = '__all__'


class DayClosingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayClosing
        fields = '__all__'


class DayClosingAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayClosingAdmin
        fields = '__all__'


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =BusinessProfile
        fields ='__all__'


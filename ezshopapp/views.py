from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .models import Shop, ShopAdmin, Role, Employee, Sale, ExpenseType, ReceiptType, Bank, ReceiptTransaction, PaymentTransaction, BankDeposit, Service, Product, EmployeeTransaction, DailySummary
from .forms import ShopForm, RoleForm, EmployeeForm, ExpenseTypeForm, ReceiptTypeForm, BankForm, ReceiptTransactionForm, PaymentTransactionForm, BankDepositForm, ServiceForm, ProductForm, EmployeeTransactionForm, DailySummaryForm
from .serializers import LoginSerializer, SaleSerializer
from django.contrib.auth.views import LogoutView, LoginView
from .forms import CustomLoginForm, SaleForm, SaleItemFormSet
from rest_framework import generics


class CustomLoginView(FormView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = '/'  

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid login credentials') 
            return super().form_invalid(form)

    def form_invalid(self, form):
       
        return super().form_invalid(form)

# class RegistrationView(FormView):
#     template_name = 'registration.html'
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')  # Redirect to login page after successful registration

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
    
class CustomLogoutView(LogoutView):
    next_page = '/login/' 

class ShopListView(ListView):
    model = Shop
    template_name = 'shop_list.html'
    context_object_name = 'shops'

    def get_queryset(self):
        # Retrieve the queryset and order it by name in ascending order
        return Shop.objects.all().order_by('-name')
    
class ShopCreateView(CreateView):
    model = Shop
    form_class = ShopForm
    template_name = 'create_shop.html'
    success_url = reverse_lazy('shop_list')

class ShopUpdateView(UpdateView):
    model = Shop
    form_class = ShopForm
    template_name = 'update_shop.html'
    success_url = reverse_lazy('shop_list')

class ShopDeleteView(DeleteView):
    model = Shop
    template_name = 'delete_shop.html'
    success_url = reverse_lazy('shop_list')


class RoleListView(ListView):
    model = Role
    template_name = 'role_list.html'

class RoleCreateView(CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'create_role.html'
    success_url = reverse_lazy('role_list')

class RoleUpdateView(UpdateView):
    model = Role
    form_class = RoleForm
    template_name = 'update_role.html'
    success_url = reverse_lazy('role_list')

class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'delete_role.html'
    success_url = reverse_lazy('role_list')

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'  # Update with the correct path to your template
    context_object_name = 'employees'  # Optional, if you want to customize the context variable name in the template

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'create_employee.html'
    success_url = reverse_lazy('employee_list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'update_employee.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'delete_employee.html'
    success_url = reverse_lazy('employee_list')


class ExpenseTypeListView(ListView):
    model = ExpenseType
    template_name = 'expense_type_list.html'

class ExpenseTypeCreateView(CreateView):
    model = ExpenseType
    form_class = ExpenseTypeForm
    template_name = 'create_expense_type.html'
    success_url = reverse_lazy('expense_type_list')

class ExpenseTypeUpdateView(UpdateView):
    model = ExpenseType
    form_class = ExpenseTypeForm
    template_name = 'update_expense_type.html'
    success_url = reverse_lazy('expense_type_list')

class ExpenseTypeDeleteView(DeleteView):
    model = ExpenseType
    template_name = 'delete_expense_type.html'
    success_url = reverse_lazy('expense_type_list')

class ReceiptTransactionListView(ListView):
    model = ReceiptTransaction
    template_name = 'receipt_transaction_list.html'

class ReceiptTransactionCreateView(CreateView):
    model = ReceiptTransaction
    form_class = ReceiptTransactionForm
    template_name = 'create_receipt_transaction.html'
    success_url = reverse_lazy('receipt_transaction_list')

class ReceiptTransactionUpdateView(UpdateView):
    model = ReceiptTransaction
    form_class = ReceiptTransactionForm
    template_name = 'update_receipt_transaction.html'
    success_url = reverse_lazy('receipt_transaction_list')

class ReceiptTransactionDeleteView(DeleteView):
    model = ReceiptTransaction
    template_name = 'delete_receipt_transaction.html'
    success_url = reverse_lazy('receipt_transaction_list')


class PaymentTransactionListView(ListView):
    model = PaymentTransaction
    template_name = 'payment_transaction_list.html'

class PaymentTransactionCreateView(CreateView):
    model = PaymentTransaction
    form_class = PaymentTransactionForm
    template_name = 'create_payment_transaction.html'
    success_url = reverse_lazy('payment_transaction_list')

class PaymentTransactionUpdateView(UpdateView):
    model = PaymentTransaction
    form_class = PaymentTransactionForm
    template_name = 'update_payment_transaction.html'
    success_url = reverse_lazy('payment_transaction_list')

class PaymentTransactionDeleteView(DeleteView):
    model = PaymentTransaction
    template_name = 'delete_payment_transaction.html'
    success_url = reverse_lazy('payment_transaction_list')


class BankDepositListView(ListView):
    model = BankDeposit
    template_name = 'bank_deposit_list.html'

class BankDepositCreateView(CreateView):
    model = BankDeposit
    form_class = BankDepositForm
    template_name = 'create_bank_deposit.html'
    success_url = reverse_lazy('bank_deposit_list')

class BankDepositUpdateView(UpdateView):
    model = BankDeposit
    form_class = BankDepositForm
    template_name = 'update_bank_deposit.html'
    success_url = reverse_lazy('bank_deposit_list')

class BankDepositDeleteView(DeleteView):
    model = BankDeposit
    template_name = 'delete_bank_deposit.html'
    success_url = reverse_lazy('bank_deposit_list')


class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'

class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'create_service.html'
    success_url = reverse_lazy('service_list')

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'update_service.html'
    success_url = reverse_lazy('service_list')

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'delete_service.html'
    success_url = reverse_lazy('service_list')


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_list')


class EmployeeTransactionListView(ListView):
    model = EmployeeTransaction
    template_name = 'employee_transaction_list.html'

class EmployeeTransactionCreateView(CreateView):
    model = EmployeeTransaction
    form_class = EmployeeTransactionForm
    template_name = 'create_employee_transaction.html'
    success_url = reverse_lazy('employee_transaction_list')

class EmployeeTransactionUpdateView(UpdateView):
    model = EmployeeTransaction
    form_class = EmployeeTransactionForm
    template_name = 'update_employee_transaction.html'
    success_url = reverse_lazy('employee_transaction_list')

class EmployeeTransactionDeleteView(DeleteView):
    model = EmployeeTransaction
    template_name = 'delete_employee_transaction.html'
    success_url = reverse_lazy('employee_transaction_list')


class DailySummaryListView(ListView):
    model = DailySummary
    template_name = 'daily_summary_list.html'

class DailySummaryCreateView(CreateView):
    model = DailySummary
    form_class = DailySummaryForm
    template_name = 'create_daily_summary.html'
    success_url = reverse_lazy('daily_summary_list')

class DailySummaryUpdateView(UpdateView):
    model = DailySummary
    form_class = DailySummaryForm
    template_name = 'update_daily_summary.html'
    success_url = reverse_lazy('daily_summary_list')

class DailySummaryDeleteView(DeleteView):
    model = DailySummary
    template_name = 'delete_daily_summary.html'
    success_url = reverse_lazy('daily_summary_list')



def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Add error handling for invalid login
                pass
    else:
        serializer = LoginSerializer()

    return render(request, 'login.html', {'serializer': serializer})


def create_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        sale_item_formset = SaleItemFormSet(request.POST, prefix='sale_items')

        if sale_form.is_valid() and sale_item_formset.is_valid():
            sale = sale_form.save()
            sale_items = sale_item_formset.save(commit=False)

            for sale_item in sale_items:
                sale_item.sale = sale
                sale_item.save()

            return redirect('sale_list')
    else:
        sale_form = SaleForm()
        sale_item_formset = SaleItemFormSet(prefix='sale_items')

    return render(request, 'create_sale.html', {'sale_form': sale_form, 'sale_item_formset': sale_item_formset})

class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        categories = [
            {
                'name': 'Shop Management',
                'links': [
                    {'label': 'Shop List', 'url_name': 'shop_list'},
                    {'label': 'Create Shop', 'url_name': 'create_shop'},
                    # {'label': 'Update Shop', 'url_name': 'update_shop', 'kwargs': {'pk': 1}},  # Replace 1 with the actual Shop PK
                    # {'label': 'Delete Shop', 'url_name': 'delete_shop', 'kwargs': {'pk': 1}},  # Replace 1 with the actual Shop PK
            ]
            },
            {
                'name': 'Role Management',
                'links': [
                    {'label': 'Role List', 'url_name': 'role_list'},
                    {'label': 'Create Role', 'url_name': 'create_role'},
                  
                ]
            },
            {
                'name': 'Employee Management',
                'links': [
                    {'label': 'Employee List', 'url_name': 'employee_list'},
                    {'label': 'Create Employee', 'url_name': 'create_employee'},
                ]
            },
            {
                'name': 'Expense Management',
                'links': [
                    {'label': 'Expense Types', 'url_name': 'expense_type_list'},
                    {'label': 'Create Expense Type', 'url_name': 'create_expense_type'},
                ]
            },
            {
                'name': 'Transaction Management',
                'links': [
                    {'label': 'Receipt Transactions', 'url_name': 'receipt_transaction_list'},
                    {'label': 'Payment Transactions', 'url_name': 'payment_transaction_list'},
                ]
            },
            {
                'name': 'Bank Management',
                'links': [
                    {'label': 'Bank Deposits', 'url_name': 'bank_deposit_list'},
                ]
            },
            {
                'name': 'Service and Product Management',
                'links': [
                    {'label': 'Service List', 'url_name': 'service_list'},
                    {'label': 'Product List', 'url_name': 'product_list'},
                ]
            },
            {
                'name': 'Employee Transaction Management',
                'links': [
                    {'label': 'Employee Transactions', 'url_name': 'employee_transaction_list'},
                ]
            },
            {
                'name': 'Daily Summary Management',
                'links': [
                    {'label': 'Daily Summaries', 'url_name': 'daily_summary_list'},
                ]
            },
            {
                'name': 'Sales Management',
                'links': [
                    {'label': 'Create Sales', 'url_name': 'create_sale'},
                    \
                  
                ]
            },
        ]

        return {'categories': categories}
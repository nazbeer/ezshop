from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.views import View
from django.forms import formset_factory
from django.contrib.auth import authenticate, login
from .models import Shop, ShopAdmin, User, Role, Employee, Sale, ExpenseType, SaleByAdminService, SalesByAdminItem, ReceiptType, Bank, SaleItem, ReceiptTransaction, PaymentTransaction, BankDeposit, Service, Product, EmployeeTransaction, DailySummary, DayClosing
from .forms import ShopForm, RoleForm, AdminProfileForm,  EmployeeForm, ExpenseTypeForm, ReceiptTypeForm, BankForm, ReceiptTransactionForm, PaymentTransactionForm, BankDepositForm, ServiceForm, ProductForm, EmployeeTransactionForm, DailySummaryForm
from .serializers import LoginSerializer, SaleSerializer
from django.contrib.auth.views import LogoutView, LoginView
from .forms import CustomLoginForm, DayClosingForm, BusinessProfileForm, AdminUserForm, SalesByStaffItemServiceForm, SaleForm, SalesByAdminItemForm, SaleByAdminServiceForm
from rest_framework import generics
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Assuming you have a form for admin users
AdminUserForm = formset_factory(AdminUserForm, extra=1)

class CustomLoginView(FormView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = '/home'  

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

def employee_list(request):
    # Get query parameter for search
    query = request.GET.get('q')
    
    # Filter employees based on search query
    if query:
        employees = Employee.objects.filter(
            Q(employee_id__icontains=query) | 
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query)
        )
    else:
        employees = Employee.objects.all()
    
    # Pagination
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    
    return render(request, 'employee_list.html', {'employees': employees})

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'create_employee.html'
    success_url = reverse_lazy('employee_list')


def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_edit.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_delete.html', {'employee': employee})


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

def create_business_profile(request):
    if request.method == 'POST':
        business_profile_form = BusinessProfileForm(request.POST, request.FILES)
        admin_profile_forms = [AdminProfileForm(request.POST, prefix=f'admin_profile_{i}') for i in range(5)]  # Assuming max 5 admins
        
        if business_profile_form.is_valid() and all([form.is_valid() for form in admin_profile_forms]):
            # Save business profile data
            business_profile = business_profile_form.save()
            
            # Save admin profiles and connect with business profile
            for form in admin_profile_forms:
                if form.cleaned_data['email'] and form.cleaned_data['mobile']:
                    admin_profile = form.save(commit=False)
                    admin_profile.business_profile = business_profile
                    admin_profile.save()
                    
                    # Connect selected employee to admin profile
                    employee_id = form.cleaned_data.get('employee')
                    if employee_id:
                        employee = Employee.objects.get(pk=employee_id)
                        admin_profile.employees.add(employee)
            
            return redirect('success_page')  # Redirect to success page after successful submission
    else:
        business_profile_form = BusinessProfileForm()
        admin_profile_forms = [AdminProfileForm(prefix=f'admin_profile_{i}') for i in range(5)]  # Assuming max 5 admins

    employees = Employee.objects.all()  # Retrieve all employees to populate select field

    return render(request, 'create_business_profile.html', {
        'business_profile_form': business_profile_form,
        'admin_profile_forms': admin_profile_forms,
        'employees': employees,
    })

def profile_created(request):
    return render(request, 'profile_created.html')

def success_view(request):
    return render(request, 'success.html')

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
    employees = Employee.objects.all()
    products = Product.objects.all()
    if request.method == 'POST':
        form = SalesByAdminItemForm(request.POST)
        if form.is_valid():
            sale = form.save()
            return HttpResponse(f'Sale created successfully with ID: {sale.id}')  # Debugging message
        else:
            #return HttpResponse('Form is not valid')  # Debugging message
            return render(request, 'success.html') 
    else:
        form = SalesByAdminItemForm()
    
    return render(request, 'sales_by_admin_item_form.html', {'form': form, 'employees': employees, 'products': products})

def sale_by_admin_service(request):
    employees = Employee.objects.all()
    services = Service.objects.all()
    
    SaleByAdminServiceFormSet = formset_factory(SaleByAdminServiceForm, extra=1)

    if request.method == 'POST':
        formset = SaleByAdminServiceFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    # Here, you need to associate each sale item with the sale
                    sale_item = form.save(commit=False)
                    # Assuming you have a field named 'sale' in SaleByAdminService model
                    # You need to associate the sale item with the sale instance before saving
                  #  sale_item.date = date
                    sale_item.save()

            # Redirect after successful form submission
            return redirect('success.html')
    else:
        formset = SaleByAdminServiceFormSet()

    return render(request, 'sales_by_admin_service.html', {'formset': formset, 'employees': employees, 'services': services})

class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

def submit_sale(request):
    form = SaleForm()
    services = Service.objects.all()
    
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            service = form.cleaned_data['service']
            quantity = form.cleaned_data['quantity']
            amount = form.cleaned_data['amount']
            discount = form.cleaned_data['discount']
            tip = form.cleaned_data['tip']
            payment_method = form.cleaned_data['payment_method']
            
    
            sale = form.save(commit=False)
            sale.save()
            
            # Redirect to a success page
            return render(request, 'success.html')
    return render(request, 'submit_sale.html', {'form': form, 'services': services})

def DayClosingView(request):
    if request.method == 'POST':
        date = request.POST['date']
        total_services = request.POST['total_services']
        total_sales = request.POST['total_sales']
        tip = request.POST.get('tip', None)
        total_collection = request.POST['total_collection']
        advance = request.POST.get('advance', None)
        net_collection = request.POST['net_collection']

        day_closing = DayClosing(
            date=date,
            total_services=total_services,
            total_sales=total_sales,
            tip=tip,
            total_collection=total_collection,
            advance=advance,
            net_collection=net_collection
        )
        try:
            day_closing.save()
            return redirect('day_closing_report')
        except Exception as e:
            print("Error saving data:", e)

    return render(request, 'dayclosing.html')

def edit_day_closing(request, pk):
    day_closing = get_object_or_404(DayClosing, pk=pk)
    if request.method == 'POST':
        form = DayClosingForm(request.POST, instance=day_closing)
        if form.is_valid():
            form.save()
            return redirect('day_closing_report')  # Redirect to day closing report page after editing
    else:
        form = DayClosingForm(instance=day_closing)
    return render(request, 'dayclosing_edit.html', {'form': form})


def day_closing_report(request):
    day_closings_list = DayClosing.objects.all()
    paginator = Paginator(day_closings_list, 10)  # Show 10 entries per page

    page = request.GET.get('page')
    try:
        day_closings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        day_closings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        day_closings = paginator.page(paginator.num_pages)

    return render(request, 'day_closing_report.html', {'day_closings': day_closings})

def approve_day_closing(request, dayclosing_id):
    dayclosing = DayClosing.objects.get(pk=dayclosing_id)
    dayclosing.status = 'approved'
    dayclosing.save()
    return redirect('day_closing_report')

def sales_by_staff_item_service(request):
    products = Product.objects.all()
    service = Service.objects.all()
    if request.method == 'POST':
        form = SalesByStaffItemServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success.html')  # Redirect to success page
    else:
        form = SalesByStaffItemServiceForm()
    return render(request, 'sales_by_staff_item_service.html', {'form': form, 'products':products, 'services':service})

def sales_report(request):
    sales_services = SaleByAdminService.objects.all()
    sales_items = SalesByAdminItem.objects.all()

    print("Sales Services:", sales_services)
    print("Sales Items:", sales_items)

    context = {
        'sales_services': sales_services,
        'sales_items': sales_items,
    }
    
    return render(request, 'sales_report.html', context)

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        categories = [
             {
                'name': 'Sales by Admin',
                'links': [
                    # {'label': 'Create Sales', 'url_name': 'create_sale'},
                     {'label': 'Sales by Admin Item', 'url_name':'sales_by_admin_item_form'},
                     {'label': 'Sales by Admin Service', 'url_name':'sales_by_admin_service'},
                    
                    
                  
                ]
            },
             {
                'name': 'Sales by Staff',
                'links': [
                    # {'label': 'Create Sales', 'url_name': 'create_sale'},
                   {'label': 'Sales by Staff - Item & Service', 'url_name':'sales_by_staff_item_service'},
                    {'label': 'Sales by Staff', 'url_name':'submit_sale'},
                    
                  
                ]
            },
             {
                'name': 'Closing & Reports',
                'links': [
                    {'label': 'Day Closing', 'url_name':'dayclosing'},
                     {'label': 'Sales Report', 'url_name':'sales_report'},
                    {'label': 'Day Closing Report', 'url_name':'day_closing_report'},
                    
                  
                ]
            },
            {
                'name': 'Shop Management',
                'links': [
                    {'label': 'Shop List', 'url_name': 'shop_list'},
                    {'label': 'Create Shop', 'url_name': 'create_shop'},
                    {'label': 'Create Business', 'url_name': 'create_business_profile'},
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
           
        ]

        return {'categories': categories}
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.views import View
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .constants import NATIONALITIES 
from django.urls import reverse
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.contrib import messages
from .models import *
from .forms import *
from .serializers import LoginSerializer, SaleSerializer
from django.contrib.auth.views import LogoutView, LoginView
from rest_framework import generics
from django.urls import get_resolver
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls.resolvers import RoutePattern

class CustomUserAddView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'admin/auth/user/add_form.html'
    success_url = reverse_lazy('admin:index')  # Redirect to admin index after user creation

custom_user_add_view = CustomUserAddView.as_view()


AdminUserForm = formset_factory(AdminUserForm, extra=1)
@login_required(login_url='login')
def sidebar(request):

    is_superuser = request.user.is_superuser
    is_admin = request.user.groups.filter(name='Admin').exists()
    is_employee = not is_superuser and not is_admin

    return render(request, 'sidebar.html', {'user': request.user, 'is_superuser': is_superuser, 'is_admin': is_admin, 'is_employee': is_employee})

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

class CustomLogoutView(LogoutView):
    next_page = '/login/' 

class ShopListView(ListView):
    model = Shop
    template_name = 'shop_list.html'
    context_object_name = 'shops'

    def get_queryset(self):

        return Shop.objects.all().order_by('-name')

# class ShopCreateView(CreateView):
#     model = Shop
#     form_class = ShopForm
#     template_name = 'create_shop.html'
#     success_url = reverse_lazy('shop_list')

#     def form_valid(self, form):
#         shop_instance = form.save(commit=False)

#         username = form.cleaned_data['username']
#         email = form.cleaned_data['email']
#         password = form.cleaned_data['password']

#         try:
#             # Check if a superuser already exists for the given shop
#             if User.objects.filter(is_superuser=True, shop=shop_instance).exists():
#                 messages.error(self.request, "A superuser already exists for this shop.")
#                 return redirect('shop_list')

#             # Create a new superuser
#             user = User.objects.create_superuser(username=username, email=email, password=password)
#             user.is_staff = True  
#             user.is_active = True
#             user.is_superuser = True  
#             user.save()

#             shop_instance.user = user
#             shop_instance.save()

#             return super().form_valid(form)
#         except IntegrityError:
#             messages.error(self.request, "An error occurred while creating the shop.")
#             return super().form_valid(form)
        

class ShopAdminCreateView(CreateView):
    model = User
    form_class = ShopAdminForm
    template_name = 'create_admin_user.html'
    success_url = '/home'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        shop = Shop.objects.create(name=user.username + "'s Shop", license_number="License-" + user.username)
        ShopAdmin.objects.create(user=user, shop=shop)
        return super().form_valid(form)

class ShopCreateView(CreateView):
    model = Shop
    form_class = ShopForm
    template_name = 'create_shop.html'
    success_url = '/login'

    def form_valid(self, form):
        shop = form.save(commit=False)
        admin_user = self.request.user
        if not ShopAdmin.objects.filter(user=admin_user).exists():
            ShopAdmin.objects.create(user=admin_user, shop=shop)
            return super().form_valid(form)
        else:
            # Only one shop can be created under each user
            return super().form_invalid(form)

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
@login_required
def create_role(request):
    if request.method == 'POST':

        role_name = request.POST.get('name')
        module_names = request.POST.getlist('modules')
        is_employee = request.POST.get('is_employee') == 'on'

        new_role = Role.objects.create(name=role_name, is_employee=is_employee)

        for module_name in module_names:
            module = Module.objects.get(name=module_name)
            new_role.modules.add(module)

        new_role.save()

        return redirect('role_list')
    else:
        modules = Module.objects.all()
        return render(request, 'create_role.html', {'modules': modules})

def analytics_view(request):

    total_employees = Employee.objects.all().count()

    total_revenue = DailySummary.objects.aggregate(total_revenue=Sum('amount'))['total_revenue']

    return render(request, 'home.html', {
        'total_employees': total_employees,
        'total_revenue': total_revenue,

    })

class RoleUpdateView(TemplateView):
    template_name = 'update_role.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role_id = kwargs.get('pk')
        role = get_object_or_404(Role, pk=role_id)
        modules = role.modules.all()  
        context['role'] = role
        context['modules'] = modules
        return context

    def post(self, request, *args, **kwargs):
        role_id = kwargs.get('pk')
        role = get_object_or_404(Role, pk=role_id)

        role_name = request.POST.get('name')
        role.name = role_name

        is_employee = request.POST.get('is_employee')
        if is_employee:
            role.is_employee = True
        else:
            role.is_employee = False

        role.save()

        return HttpResponseRedirect(reverse('role_list'))

class RoleDeleteView(DeleteView):
    model = Role
    template_name = 'delete_role.html'
    success_url = reverse_lazy('role_list')

@login_required(login_url='login')
def create_expense_type(request):
    if request.method == 'POST':
        form = ExpenseTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_type_list')
    else:
        form = ExpenseTypeForm()
    return render(request, 'create_expense_type.html', {'form': form})

def employee_list(request):
    query = request.GET.get('q')
    if query:
        employees = Employee.objects.filter(
            Q(employee_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(second_name__icontains=query)
        )
    else:
        employees = Employee.objects.all()

    paginator = Paginator(employees, 10)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'employee_list.html', {'employees': employees})

def create_employee(request):
    error_occurred = False  
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                employee = form.save(commit=False)
                employee.save()
                return redirect('employee_list') 
            except Exception as e:
                print("An error occurred while saving the form:", e)
                error_occurred = True  
                messages.error(request, "An error occurred while saving the form.")
    else:
        form = EmployeeForm()

    business_profiles = BusinessProfile.objects.all()
    context = {
        'form': form,
        'business_profiles': business_profiles,
        'error_occurred': error_occurred,
        'nationalities': NATIONALITIES,  # Pass NATIONALITIES to the template context
    }
    return render(request, 'create_employee.html', context)

def get_employee_data(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    data = {
        'total_services': employee.total_services,
        'total_sales': employee.total_sales,
    }
    return JsonResponse(data)

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

def create_bank_deposit(request):
    if request.method == 'POST':
        form = BankDepositForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_deposit_list')  
    else:
        form = BankDepositForm()

    context = {
        'form': form,
    }
    return render(request, 'create_bank_deposit.html', context)

class BankListView(ListView):
    model = Bank
    template_name = 'bank_list.html'

def create_bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_list')  
    else:
        form = BankForm()

    context = {
        'form': form,
    }
    return render(request, 'create_bank.html', context)

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

    def form_valid(self, form):

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('service_list') 

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

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'update_product.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_list')

def employee_transaction_create(request):
    if request.method == 'POST':
        form = EmployeeTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  
    else:
        form = EmployeeTransactionForm()
    return render(request, 'create_employee_transaction.html', {'form': form})

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

def get_shop_details(request, name):
    try:
        shop = Shop.objects.get(name=name)

        return JsonResponse({
            'shop_name': shop.name,
            'license_number': shop.license_number,

        })
    except Shop.DoesNotExist:
        return JsonResponse({'error': 'Shop not found'}, status=404)
@login_required
def create_business_profile(request):
    if request.method == 'POST':
        business_profile_form = BusinessProfileForm(request.POST, request.FILES)
        if business_profile_form.is_valid():
            business_profile = business_profile_form.save(commit=False)
            business_profile.save()
            return redirect('success')
        else:
            # Form is not valid, display form with errors
            messages.error(request, "Please correct the errors below.")
    else:
        business_profile_form = BusinessProfileForm()

    context = {'business_profile_form': business_profile_form}
    if request.user.is_authenticated:
        # Fetch the shop details associated with the logged-in user
        try:
            shop_admin = ShopAdmin.objects.get(user=request.user)
            context['shop_details'] = shop_admin.shop
            context['license_number'] = shop_admin.shop.license_number
        except ShopAdmin.DoesNotExist:
            context['shop_details'] = None
            context['license_number'] = None

    return render(request, 'create_business_profile.html', context)


def edit_business_profile(request, pk):
    business_profile = get_object_or_404(BusinessProfile, pk=pk)
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES, instance=business_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business profile updated successfully.')
            return redirect('business_profile_list')
    else:
        form = BusinessProfileForm(instance=business_profile)
    return render(request, 'edit_business_profile.html', {'form': form})

def delete_business_profile(request, pk):
    business_profile = get_object_or_404(BusinessProfile, pk=pk)
    if request.method == 'POST':
        business_profile.delete()
        messages.success(request, 'Business profile deleted successfully.')
        return redirect('business_profile_list')
    return render(request, 'delete_business_profile.html', {'business_profile': business_profile})

def fetch_shop_details(request):
    shop_id = request.GET.get('shop_id')
    if shop_id:
        try:
            shop = Shop.objects.get(pk=shop_id)
            print(shop)

            data = {
                'license_number': '2455',

            }

            return JsonResponse(data)
        except Shop.DoesNotExist:
            return JsonResponse({'error': 'Shop not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def business_profile_list(request):
    profiles = BusinessProfile.objects.all()
    return render(request, 'business_profile_list.html', {'profiles': profiles})

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
            return HttpResponse(f'Sale created successfully with ID: {sale.id}')  
        else:

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
                    sale = form.save(commit=False)
                    sale.save()
            return redirect('success.html')
    else:
        formset = SaleByAdminServiceFormSet()

    return render(request, 'sales_by_admin_service.html', {'formset': formset, 'employees': employees, 'services': services})

def sale_by_admin_service(request):

    sales_services = SaleByAdminService.objects.all()
    sales_items = SalesByAdminItem.objects.all()

    return render(request, 'sales_by_admin_service.html', {'sales_services': sales_services, 'sales_items': sales_items})

class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

def submit_sale(request):
    form = SaleForm()
    services = Service.objects.all()

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():

            service = form.cleaned_data['service']
            quantity = form.cleaned_data['quantity']
            amount = form.cleaned_data['amount']
            discount = form.cleaned_data['discount']

            payment_method = form.cleaned_data['payment_method']

            sale = form.save(commit=False)
            sale.save()

            return render(request, 'success')
    return render(request, 'submit_sale.html', {'form': form, 'services': services})

def DayClosingView(request):
    if request.method == 'POST':
        form = DayClosingForm(request.POST)

        if form.is_valid():

            date = form.cleaned_data['date']
            total_services = form.cleaned_data['total_services']
            total_sales = form.cleaned_data['total_sales']
            total_collection = form.cleaned_data['total_collection']
            advance = form.cleaned_data['advance']
            net_collection = form.cleaned_data['net_collection']

            employee = form.cleaned_data['employee']

            employee_transactions = EmployeeTransaction.objects.filter(employee=employee)

            day_closing = DayClosing.objects.create(
                date=date,
                total_services=total_services,
                total_sales=total_sales,
                total_collection=total_collection,
                advance=advance,
                net_collection=net_collection
            )

            day_closing.employee_transactions.set(employee_transactions)
            day_closing.save()
            return redirect('day_closing_report')
    else:
        form = DayClosingForm()

    return render(request, 'dayclosing.html', {'form': form})

def day_closing_admin(request):
    if request.method == 'POST':
        form = DayClosingFormAdmin(request.POST)
        if form.is_valid():

            date = timezone.now().date()  
            total_collection = form.cleaned_data['total_collection']
            advance = form.cleaned_data['advance']
            net_collection = form.cleaned_data['net_collection']

            day_closing_admin = DayClosingAdmin(
                date=date,
                total_collection=total_collection,
                advance=advance,
                net_collection=net_collection,
                **DayClosingAdmin.calculate_totals()
            )
            day_closing_admin.save()
            return redirect('day_closing_report')
    else:
        form = DayClosingFormAdmin(initial={'date': timezone.now().date()})  

    return render(request, 'dayclosing_admin.html', {'form': form})

def edit_day_closing(request, pk):
    day_closing = get_object_or_404(DayClosing, pk=pk)
    if request.method == 'POST':
        form = DayClosingForm(request.POST, instance=day_closing)
        if form.is_valid():
            form.save()
            return redirect('day_closing_report')  
    else:
        form = DayClosingForm(instance=day_closing)
    return render(request, 'dayclosing_edit.html', {'form': form})

def day_closing_report(request):
    day_closings_list = DayClosing.objects.all()
    paginator = Paginator(day_closings_list, 10)  

    page = request.GET.get('page')
    try:
        day_closings = paginator.page(page)
    except PageNotAnInteger:

        day_closings = paginator.page(1)
    except EmptyPage:

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
            return redirect('success.html')  
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

def create_receipt_transaction(request):
    if request.method == 'POST':
        form = ReceiptTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receipt_transaction_list')  
    else:
        form = ReceiptTransactionForm()
    return render(request, 'create_receipt_transaction.html', {'form': form})

def create_receipt_type(request):
    if request.method == "POST":
        form = ReceiptTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_receipt_transaction')  
    else:
        form = ReceiptTypeForm()
    return render(request, 'create_receipt_type.html', {'form': form})

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Fetch the shop details associated with the logged-in user
            try:
                shop_admin = ShopAdmin.objects.get(user=self.request.user)
                context['shop'] = shop_admin.shop
            except ShopAdmin.DoesNotExist:
                context['shop'] = None
        total_employees = Employee.objects.all().count()
        total_business = BusinessProfile.objects.all().count()
        num_products = Product.objects.all().count()
        categories = [
             {
                'name': 'Shop Management',
                'links': [

                    {'label': 'Create Business', 'url_name': 'create_business_profile'},
                    {'label': 'Business Profiles', 'url_name': 'business_profile_list'},
            ]
            },
            {
                'name': 'Service and Product Management',
                'links': [
                    {'label': 'Service List', 'url_name': 'service_list'},
                    {'label': 'Product List', 'url_name': 'product_list'},
                    {'label': 'Create Product', 'url_name': 'create_product'},
                    {'label': 'Create Service', 'url_name': 'create_service'},
                ]
            },
            {
                'name': 'Sales by Admin',
                'links': [
                     {'label': 'Sales by Admin Item', 'url_name':'sales_by_admin_item_form'},
                     {'label': 'Sales by Admin Service', 'url_name':'sales_by_admin_service'},
                ]
            },
            {
                'name': 'Sales by Staff',
                'links': [
                   {'label': 'Sales by Staff - Item & Service', 'url_name':'sales_by_staff_item_service'},
                    {'label': 'Sales by Staff', 'url_name':'submit_sale'},
                ]
            },
            {
                'name': 'Closing & Reports',
                'links': [
                    {'label': 'Day Closing', 'url_name':'dayclosing'},
                    {'label': 'Day Closing by Admin', 'url_name':'dayclosing_admin'},
                    {'label': 'Sales Report', 'url_name':'sales_report'},
                    {'label': 'Day Closing Report', 'url_name':'day_closing_report'},
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
                'name': 'Employee Transaction Management',
                'links': [
                    {'label': 'Employee Transactions', 'url_name': 'employee_transaction_list'},
                    {'label': 'Create Transactions', 'url_name': 'create_employee_transaction'},
                ]
            },
            {
                'name': 'Daily Summary Management',
                'links': [
                    {'label': 'Daily Summaries', 'url_name': 'daily_summary_list'},
                ]
            },
        ]

        return {'categories': categories, 'total_employees': total_employees, 'total_business': total_business, 'num_products':num_products, **context }
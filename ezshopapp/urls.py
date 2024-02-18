from django.urls import path
from .views import (
    ShopListView, ShopCreateView, ShopUpdateView, ShopDeleteView,
    RoleListView, RoleCreateView, RoleUpdateView, RoleDeleteView,
    EmployeeCreateView, 
    ExpenseTypeListView, ExpenseTypeCreateView, ExpenseTypeUpdateView, ExpenseTypeDeleteView,
    ReceiptTransactionListView, ReceiptTransactionCreateView, ReceiptTransactionUpdateView, ReceiptTransactionDeleteView,
    PaymentTransactionListView, PaymentTransactionCreateView, PaymentTransactionUpdateView, PaymentTransactionDeleteView,
    BankDepositListView, BankDepositCreateView, BankDepositUpdateView, BankDepositDeleteView,
    ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    EmployeeTransactionListView, EmployeeTransactionCreateView, EmployeeTransactionUpdateView, EmployeeTransactionDeleteView,
    DailySummaryListView, DailySummaryCreateView, DailySummaryUpdateView, DailySummaryDeleteView, CustomLoginView, HomeView, CustomLogoutView, SaleListCreateView, submit_sale, DayClosingView,
    day_closing_report, approve_day_closing, employee_list, create_sale, sale_by_admin_service, sales_report, success_view, sales_by_staff_item_service, create_business_profile, profile_created,
    employee_edit, employee_delete

)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('create-profile/', create_business_profile, name='create_business_profile'),
    path('profile-created/', profile_created, name='profile_created'),
   # path('register/', RegistrationView.as_view(), name='register'),
    # Shop URLs
    #path('sale/create/', create_sale, name='create_sale'),
    path('shop/', ShopListView.as_view(), name='shop_list'),
    path('shop/create/', ShopCreateView.as_view(), name='create_shop'),
    path('shop/update/<int:pk>/', ShopUpdateView.as_view(), name='update_shop'),
    path('shop/delete/<int:pk>/', ShopDeleteView.as_view(), name='delete_shop'),
    path('sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    # path('sale/create/', create_sale, name='sales_by_admin_item_form'),
    path('sale/salesbystaff/', submit_sale, name='submit_sale'),
    path('sale/dayclosing/',  DayClosingView, name='dayclosing'),
    path('sale/day-closing-report/', day_closing_report, name='day_closing_report'),
    path('sale/day-closing-report/<int:dayclosing_id>/approve/', approve_day_closing, name='approve_day_closing'),
    path('sale/', create_sale, name='sales_by_admin_item_form'),
    path('sale/success/', success_view, name='success'),
    path('sale/sales-by-staff-item-service/', sales_by_staff_item_service, name='sales_by_staff_item_service'),
    path('sale/sales-by-admin-service', sale_by_admin_service, name='sales_by_admin_service'),
    path('sale/sales-report/', sales_report, name='sales_report'),
    # Role URLs
    path('role/', RoleListView.as_view(), name='role_list'),
    path('role/create/', RoleCreateView.as_view(), name='create_role'),
    path('role/update/<int:pk>/', RoleUpdateView.as_view(), name='update_role'),
    path('role/delete/<int:pk>/', RoleDeleteView.as_view(), name='delete_role'),

    # Employee URLs
    path('employee/', employee_list, name='employee_list'),
    path('employee/create/', EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/<int:pk>/edit/', employee_edit, name='employee_edit'),
     path('employees/<int:pk>/delete/', employee_delete, name='employee_delete'),

    # ExpenseType URLs
    path('expense-type/', ExpenseTypeListView.as_view(), name='expense_type_list'),
    path('expense-type/create/', ExpenseTypeCreateView.as_view(), name='create_expense_type'),
    path('expense-type/update/<int:pk>/', ExpenseTypeUpdateView.as_view(), name='update_expense_type'),
    path('expense-type/delete/<int:pk>/', ExpenseTypeDeleteView.as_view(), name='delete_expense_type'),

    # ReceiptTransaction URLs
    path('receipt-transaction/', ReceiptTransactionListView.as_view(), name='receipt_transaction_list'),
    path('receipt-transaction/create/', ReceiptTransactionCreateView.as_view(), name='create_receipt_transaction'),
    path('receipt-transaction/update/<int:pk>/', ReceiptTransactionUpdateView.as_view(), name='update_receipt_transaction'),
    path('receipt-transaction/delete/<int:pk>/', ReceiptTransactionDeleteView.as_view(), name='delete_receipt_transaction'),

    # PaymentTransaction URLs
    path('payment-transaction/', PaymentTransactionListView.as_view(), name='payment_transaction_list'),
    path('payment-transaction/create/', PaymentTransactionCreateView.as_view(), name='create_payment_transaction'),
    path('payment-transaction/update/<int:pk>/', PaymentTransactionUpdateView.as_view(), name='update_payment_transaction'),
    path('payment-transaction/delete/<int:pk>/', PaymentTransactionDeleteView.as_view(), name='delete_payment_transaction'),

    # BankDeposit URLs
    path('bank-deposit/', BankDepositListView.as_view(), name='bank_deposit_list'),
    path('bank-deposit/create/', BankDepositCreateView.as_view(), name='create_bank_deposit'),
    path('bank-deposit/update/<int:pk>/', BankDepositUpdateView.as_view(), name='update_bank_deposit'),
    path('bank-deposit/delete/<int:pk>/', BankDepositDeleteView.as_view(), name='delete_bank_deposit'),

    # Service URLs
    path('service/', ServiceListView.as_view(), name='service_list'),
    path('service/create/', ServiceCreateView.as_view(), name='create_service'),
    path('service/update/<int:pk>/', ServiceUpdateView.as_view(), name='update_service'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='delete_service'),

    # Product URLs
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),

    # EmployeeTransaction URLs
    path('employee-transaction/', EmployeeTransactionListView.as_view(), name='employee_transaction_list'),
    path('employee-transaction/create/', EmployeeTransactionCreateView.as_view(), name='create_employee_transaction'),
    path('employee-transaction/update/<int:pk>/', EmployeeTransactionUpdateView.as_view(), name='update_employee_transaction'),
    path('employee-transaction/delete/<int:pk>/', EmployeeTransactionDeleteView.as_view(), name='delete_employee_transaction'),

    # DailySummary URLs
    path('daily-summary/', DailySummaryListView.as_view(), name='daily_summary_list'),
    path('daily-summary/create/', DailySummaryCreateView.as_view(), name='create_daily_summary'),
    path('daily-summary/update/<int:pk>/', DailySummaryUpdateView.as_view(), name='update_daily_summary'),
    path('daily-summary/delete/<int:pk>/', DailySummaryDeleteView.as_view(), name='delete_daily_summary'),
]

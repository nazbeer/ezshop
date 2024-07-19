from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *
from . import appviews
from rest_framework.routers import DefaultRouter
from rest_framework import routers, serializers, viewsets
from django.conf.urls import handler404

router = routers.DefaultRouter()
router.register(r'day-closings', appviews.DayClosingViewSet, basename='day-closings')
router.register(r'day-closings-admin', appviews.DayClosingAdminViewSet, basename='day-closings-admin')
router.register(r'sales-by-staff-service', appviews.SaleByStaffServiceViewSet, basename='sales-by-staff-service')
router.register(r'sales-by-staff-item', appviews.SaleByStaffItemViewSet, basename='sales-by-staff-item')
router.register(r'sales-by-staff-item-service', appviews.SalesByStaffItemServiceViewSet, basename='sales-by-staff-item-service')
router.register(r'employee-profile', appviews.EmployeeProfileViewSet, basename='employee-profile')



# Register new APIs
# router.register(r'employeelogin', EmployeeLoginAPIView, basename='employeelogin')
# router.register(r'employeelogout', EmployeeLogoutAPIView, basename='employeelogout')
#router.register(r'employeedashboard', appviews.EmployeeDashboardAPIView.as_view(), basename='employeedashboard')
# router.register(r'employeeprofile', EmployeeProfileAPIView, basename='employeeprofile')
# router.register(r'dayclosingreport', DayClosingReportAPIView, basename='dayclosingreport')
# router.register(r'salesreport', SalesReportAPIView, basename='salesreport')


urlpatterns = [
    path('api/', include((router.urls, 'api'), namespace='api')),
    path('api/v2/', include((router.urls, 'api_v2'), namespace='api_v2')),
    path('send_message/', send_message, name='send_message'),
    # path('api/employees/login/<str:username>/<str:password>/', EmployeeViewSet.as_view({'post': 'loginapi'}), name='employee_login'),
    # path('api/employees/employee_dashboard/', EmployeeViewSet.as_view({'get': 'employee_dashboard'}), name='employee_dashboard'),
    # path('api/employees/profile/', EmployeeViewSet.as_view({'get': 'profile'}), name='profile'),
    # path('api/employees/logout/', EmployeeViewSet.as_view({'post': 'logout'}), name='logout'),

    path('get-employee-transaction-window/', get_employee_transaction_window, name='get_employee_transaction_window'),


    path('clearcache/', views.clear_cache_admin, name='clearcache_admin'),
    path('', salonview, name='index'),
    path('about/', aboutview, name='about'),
    path('landing/', landingview, name='landing'),
    path('feature/', featureview, name='feature'),
    path('contact/', contact_view, name='contact'),


    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('error/', error_view, name='error'),
    path('reset_session_timeout/', reset_session_timeout, name='reset_session_timeout'),
    path('sidebar/', sidebar, name='sidebar'),
    path('home/', HomeView.as_view(), name='home'),
    path('admin/auth/user/add/', custom_user_add_view, name='custom_user_add'),
    path('create-business-profile/', create_business_profile, name='create_business_profile'),
    path('fetch_shop_details/', fetch_shop_details, name='fetch_shop_details'),
    path('profile-created/', profile_created, name='profile_created'),
    path('business/', business_profile_list, name='business_profile_list'),
    path('business_profiles/<int:pk>/edit/', edit_business_profile, name='edit_business_profile'),
    path('business_profiles/<int:pk>/delete/', delete_business_profile, name='delete_business_profile'),
    # path('calculate-summary/', calculate_summary, name='calculate_summary'),
    path('get_shop_details/<str:name>/', get_shop_details, name='get_shop_details'),
    path('shop/', ShopListView.as_view(), name='shop_list'),
    path('shop/create/', ShopCreateView.as_view(), name='create_shop'),
    path('shop/update/<int:pk>/', ShopUpdateView.as_view(), name='update_shop'),
    path('shop/delete/<int:pk>/', ShopDeleteView.as_view(), name='delete_shop'),
   # path('sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    
    path('get_employee_data/<int:employee_id>/', get_employee_data, name='get_employee_data'),
    path('dayclosing/admin/', day_closing_admin, name='dayclosing_admin'),

    path('fetch-data-admin/<str:selected_date>/<int:employee_id>/', fetch_data_admin, name='fetch_data_admin'),
    path('fetch-remaining-employees/<str:selected_date>/<int:employeeId>/', views.fetch_remaining_employees, name='fetch_remaining_employees'),

    path('sale/dayclosing/<int:pk>/edit/', edit_day_closing, name='edit_day_closing'),
    path('sale/day-closing-report/<int:dayclosing_id>/approve/', approve_day_closing, name='approve_day_closing'),
    path('sale/day-closing-admin-report/', day_closing_admin_report, name='day_closing_admin_report'),
    path('sale/sales_by_admin_item/', sales_by_admin_item, name='sales_by_admin_item'),
    path('sale/success/', success_view, name='success'),
    path('sale/sales-by-admin-service/', sale_by_admin_service, name='sales_by_admin_service'),
    path('sale/sales-report-admin/', sales_report_admin, name='sales_report_admin'),
    path('update_item_sales_data/', update_item_sales_data, name='update_item_sales_data'),
    path('update_service_sales_data/', update_service_sales_data, name='update_service_sales_data'),
   
    path('export_sales_report_admin_pdf/', ExportSalesReportAdminPDF.as_view(), name='export_sales_report_admin_pdf'),
    path('role/', RoleListView.as_view(), name='role_list'),
    path('role/create/', create_role, name='create_role'),
    path('role/update/<int:pk>/', RoleUpdateView.as_view(), name='update_role'),
    path('role/delete/<int:pk>/', RoleDeleteView.as_view(), name='delete_role'),
    path('employee/', employee_list, name='employee_list'),
    path('employee/create/', create_employee, name='create_employee'),
    path('check-username-availability/', check_username_availability, name='check_username_availability'),
    path('employees/<int:pk>/edit/', employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', employee_delete, name='employee_delete'),
    path('expense-type/', ExpenseTypeListView.as_view(), name='expense_type_list'),
    path('expense-type/create/', create_expense_type, name='create_expense_type'),
    path('expense-type/<int:pk>/edit/', ExpenseTypeUpdateView.as_view(), name='edit_expense_type'),
    path('expense-type/<int:pk>/delete/', ExpenseTypeDeleteView.as_view(), name='delete_expense_type'),
    path('receipt-type/create/', create_receipt_type, 
    name='create_receipt_type'),
    path('receipt-type/', receipt_type_list, name='receipt_type_list'),
    # path('receipt-type/', ReceiptTypeListView.as_view(), name='receipt_type_list'),

    
    path('receipt-transaction/', ReceiptTransactionListView.as_view(), name='receipt_transaction_list'),
    path('receipt-transaction/create/', create_receipt_transaction, name='create_receipt_transaction'),
    path('receipt-transaction/update/<int:pk>/', ReceiptTransactionUpdateView.as_view(), name='update_receipt_transaction'),
    path('receipt-transaction/delete/<int:pk>/', ReceiptTransactionDeleteView.as_view(), name='delete_receipt_transaction'),
    path('payment-transaction/', PaymentTransactionListView.as_view(), name='payment_transaction_list'),
    path('payment-transaction/create/', create_payment_transaction, name='create_payment_transaction'),
    # path('payment-transaction/create/', PaymentTransactionCreateView.as_view(), name='create_payment_transaction'),
    path('payment-transaction/update/<int:pk>/', PaymentTransactionUpdateView.as_view(), name='update_payment_transaction'),
    path('payment-transaction/delete/<int:pk>/', PaymentTransactionDeleteView.as_view(), name='delete_payment_transaction'),
    path('bank/create/', create_bank, name='create_bank'),
    path('banks/', BankListView.as_view(), name='bank_list'),
    path('bank-deposit/', BankDepositListView.as_view(), name='bank_deposit_list'),
    path('bank-deposit/create/', create_bank_deposit, name='create_bank_deposit'),
    path('bank-deposit/update/<int:pk>/', BankDepositUpdateView.as_view(), name='update_bank_deposit'),
    path('bank-deposit/delete/<int:pk>/', BankDepositDeleteView.as_view(), name='delete_bank_deposit'),
    path('service/', ServiceListView.as_view(), name='service_list'),
    path('service/create/', create_service, name='create_service'),
    path('service/update/<int:pk>/', ServiceUpdateView.as_view(), name='update_service'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='delete_service'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('employee-transaction/', EmployeeTransactionListView.as_view(), name='employee_transaction_list'),
    path('employee-transaction/create/', employee_transaction_create, name='create_employee_transaction'),
    path('employee-transaction/update/<int:pk>/', EmployeeTransactionUpdateView.as_view(), name='update_employee_transaction'),
    path('employee-transaction/delete/<int:pk>/', EmployeeTransactionDeleteView.as_view(), name='delete_employee_transaction'),
    path('daily-summary/', DailySummaryListView.as_view(), name='daily_summary_list'),
    path('daily-summary/create/', DailySummaryCreate, name='daily_summary_create'),
    path('fetch-summary-data/<str:date>/', fetch_summary_data, name='fetch_summary_data'),
    path('send-daily-summary-email/', send_daily_summary_email, name='send_daily_summary_email'),
    path('daily-summary/update/<int:pk>/', DailySummaryUpdateView.as_view(), name='update_daily_summary'),
    path('daily-summary/delete/<int:pk>/', DailySummaryDeleteView.as_view(), name='delete_daily_summary'),
    path('get-daily-summary-exist/<str:date>/', get_daily_summary_exist, name='get_daily_summary_exist'),

    path('generate_invoice/<int:id>/<str:type>/', generate_invoice_pdf, name='generate_invoice_pdf'),



    path('last_day_closing/<int:employee_id>/', last_day_closing_day, name='last_day_closing_day'),
    path('last_daliy_summary/<int:employee_id>/', last_daliy_summary, name='last_daliy_summary'),
    path('dayclosing_exists/<str:date>/<int:business_profile_id>/',dayclosing_exists_for_transactions, name='dayclosing_exists_for_transactions'),



    ##### EMployee dashboard

    path('employee-login/', employee_login, name='employee_login'),
    path('employee-logout/', employee_logout, name='employee_logout'),
    path('employee-dashboard/', employee_dashboard, name='employee_dashboard'),
    path('sale/sales-by-staff-item-service/', sales_by_staff_item_service, name='sales_by_staff_item_service'),
    path('sale/sales-by-staff-service/', submit_sale, name='sales-by-staff-service'),
    path('sale/sales-by-staff-item/', sales_by_staff_item, name='sales_by_staff_item'),
    path('sale/sales-report/', sales_report, name='sales_report'),
    path('sale/dayclosing/', DayClosingCreate, name='dayclosing'),
    path('fetch-data/<int:employee_id>/', fetch_data, name='fetch_data'),
    path('sale/day-closing-report/', day_closing_report, name='day_closing_report'),
    path('profile/', employee_profile, name='employee_profile'),
    path('sidebar_emp/', sidebar_emp, name='sidebar_emp'),
    path('module/<int:module_id>/', module_detail, name='module_detail'), 


    path('bank/update/<int:pk>/', BankUpdateView.as_view(), name='update_bank'),
    path('receipt-type/update/<int:pk>/', ReceiptTypeUpdateView.as_view(), name='update_receipt_type'),


    path('notifications/', notification_view, name='notifications'),
    path('update_chart_data/', HomeView.as_view(), name='update_chart_data'),

    # Employee Api
    path('api/employees-login/', appviews.EmployeeLoginAPIView.as_view(), name='employees_login'),
    path('api/employees-logout/', appviews.EmployeeLogoutAPIView.as_view(), name='employees_logout'),
    path('api/employees-dashboard/<int:pk>/', appviews.EmployeeDashboardAPIView.as_view(), name='employees_dashboard'),
    path('api/employees-profile/<int:pk>/', appviews.EmployeeProfileAPIView.as_view(), name='employees-profile'),

    #Employee sales (product,services,product-service)
    path('api/employees-sales-by-service/<int:pk>/', appviews.SaleByStaffServiceListCreateAPIView.as_view(), name='employees_sales_by_service_create_list'),
    path('api/employees-sales-by-service/update/<int:pk>/', appviews.SaleByStaffServiceRetrieveUpdateDestroyAPIView.as_view(), name='employees_sales_by_service_update_delete'),
    path('api/employees-sales-by-item/<int:pk>/', appviews.SaleByStaffItemListCreateAPIView.as_view(), name='employees_sales_by_item_create_list'),
    path('api/employees-sales-by-item/update/<int:pk>/', appviews.SaleByStaffItemRetrieveUpdateDestroyAPIView.as_view(), name='employees_sales_by_item_update_delete'),

    path('api/employees-sales-by-item-service/<int:pk>/', appviews.SalesByStaffItemServiceListCreateAPIView.as_view(), name='employees_sales_by_item_service_list'),
    path('api/employees-sales-by-item-service/update/<int:pk>/', appviews.SalesByStaffItemServiceRetrieveUpdateDestroyAPIView.as_view(), name='employees_sales_by_item_servie_update_delete'),

    #Employee DayClosing

    path('api/employees-day-closing/create/<int:pk>/',appviews.DayClosingListCreateAPIView.as_view(), name='employees_day_closing_create'),
    path('api/employees-day-closing/update/<int:pk>/',appviews.DayClosingRetrieveUpdateDestroyAPIView.as_view(), name='employees_day_closing_update'),

    # Employee DayClosingAdmin

    path('api/employees-day-closing-admin/create/<int:pk>/',appviews.DayClosingAdminListCreateAPIView.as_view(), name='employees_day_closing_update'),
    path('api/employees-day-closing-admin/update/<int:pk>/',appviews.DayClosingAdminRetrieveUpdateDestroyAPIView.as_view(), name='employees_day_closing_admin_update'),

    path('api/employees-daily-summary/create/<int:pk>/',appviews.DailySummaryListCreateAPIView.as_view(), name='employees_daily_summary_create'),
    path('api/employees-daily-summary/update/<int:pk>/',appviews.DailySummaryRetrieveUpdateDestroyAPIView.as_view(), name='employees_daily_summary_update'),
    path('api/fetch-employees-daily-summary/<int:pk>/<str:date>/',appviews.FetchDailySummary.as_view(), name='fetch_employees_daily_summary'),

    # Employee sales and day closing reports and fetch-total-sales

    path('api/employees-sales-report/<int:pk>/',appviews.SalesReportAPIView.as_view(), name='employees_sales_report'),
    path('api/fetch-total-sale/<int:pk>/<str:date>/', appviews.fetch_total_sale, name='fetch_total_sale'),
    path('api/employees-dayclosing-report/<int:pk>/',appviews.DayClosingReportAPIView.as_view(), name='employees_dayclosing_report'),

    # product and service list
    path('api/employees/products/<int:pk>/', appviews.ProductListView.as_view(), name='employees-product-list'),
    path('api/employees/service/<int:pk>/', appviews.ServiceListView.as_view(), name='employees-service-list'),
    path('api/employees/products/<int:pk>/', appviews.ProductDetailsView.as_view(), name='employees-product-detail'),  
    path('api/employees/service/<int:pk>/', appviews.ServiceDetailsView.as_view(), name='employees-service-detail'),
    path('api/employees/job-role/<int:pk>/', appviews.JobRoleApiView.as_view(), name='employees-job-role'),

    path('api/employees/invoice/<int:id>/<str:type>/', appviews.GenerateInvoicePDF.as_view(), name='employee-invoice'),


    path('api/employees/invoice_details/<int:id>/<str:type>/', appviews.InvoiceDetailsAPIView.as_view(), name='invoice_details'),
    path('api/employees/dayclosing_pending_employee_list/<int:business_id>/<str:date>/', appviews.DayClosingPendingEmployeeList.as_view(), name='admin_day_closing_employee_list'),

    path('api/employees/business_profile/<int:pk>/', appviews.BusinessProfileApiView.as_view(), name='business_profile_details'),

    path('api/employees/<int:employee_id>/<int:year>/<int:month>/', appviews.SalesReportPdfApiView.as_view(), name='employee_sales_report_pdf'),

    path('api/employees_list/<int:business_profile_id>/', appviews.AllEmployeeListApiView.as_view(),name="business_profile_employee_list"),

    # path('api/employee/last_day_closing/<int:pk>/', appviews.LastDayClosingDateView.as_view(), name='last_day_closing'),
    path('api/employee/last_day_closing/<int:employee_id>/', appviews.LastDayClosingDateView.as_view(), name='employee_last_day_closing'),
    path('api/employee/last_daily_summary/<int:employee_id>/', appviews.LastDaliySummaryDateView.as_view(), name='employee_last_daily_summary'),
    

    path('api/employee/sales_report_pdf/<int:pk>/<str:start_date>/<str:end_date>/', appviews.SalesReportPdfAPIView.as_view(), name='employee_sales_report_pdf'),
    path('api/employee/day_closing_report_pdf/<int:pk>/<str:start_date>/<str:end_date>/', appviews.DayClosingReportPdfAPIView.as_view(), name='employee_day_closing_report_pdf'),
    path('api/employee/daily_summary_report_pdf/<int:pk>/<str:start_date>/<str:end_date>/', appviews.DailySummaryReportPdfAPIView.as_view(), name='employee_daily_summary_report_pdf'),
    path('api/employee/comission_report_pdf/<int:employee_id>/<str:start_date>/<str:end_date>/', appviews.CommissionReportAPIViewPdf.as_view(), name='employee_commission_report_pdf'),




    path('api/employee/expense_type/<int:business_profile_id>/', appviews.ExpenseTypeListCreateAPIView.as_view(), name='employee_expense_type'),
    path('api/employee/expense_type/update/<int:pk>/', appviews.ExpenseTypeRetrieveUpdateDestroyAPIView.as_view(), name='employee_expense_type_update'),

    path('api/employee/receipt_type/<int:business_profile_id>/', appviews.ReceiptTypeListCreateAPIView.as_view(), name='employee_receipt_type'),
    path('api/employee/receipt_type/update/<int:pk>/', appviews.ReceiptTypeRetrieveUpdateDestroyAPIView.as_view(), name='employee_receipt_type_update'),


    path('api/employee/expense_transaction/<int:business_profile_id>/', appviews.ExpenseTransactionListCreateAPIView.as_view(), name='employee_expense_transaction'),
    path('api/employee/expense_transaction/update/<int:pk>/', appviews.ExpenseTransactionRetrieveUpdateDestroyAPIView.as_view(), name='employee_expense_transaction_update'),

    path('api/employee/receipt_transaction/<int:business_profile_id>/', appviews.ReceiptTransactionListCreateAPIView.as_view(), name='employee_receipt_transaction'),
    path('api/employee/receipt_transaction/update/<int:pk>/', appviews.ReceiptTransactionRetrieveUpdateDestroyAPIView.as_view(), name='employee_receipt_transaction_update'),

    path('api/employee/bank_deposit_transaction/<int:business_profile_id>/', appviews.BankDepositTransactionListCreateAPIView.as_view(), name='employee_bank_deposit_transaction'),
    path('api/employee/bank_deposit_transaction/update/<int:pk>/', appviews.BankDepositRetrieveUpdateDestroyAPIView.as_view(), name='employee_bank_deposit_transaction_update'),
    path('api/employee/bank/list/<int:business_profile_id>/', appviews.BankListAPIView.as_view(), name='employee_bank_list_apiview'),

    







    #Errors
    path('error/', views.error_page, name='error_page'),
]

#handler404 = 'ezshopapp.views.handler404'
# handler404 = views.error_404,
# handler500 = views.error_500,
handler404 = views.not_found_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
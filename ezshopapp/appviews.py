from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from .forms import EmployeeLoginForm
import calendar
from django.db.models import Sum
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import generics
from django.template.loader import get_template
from xhtml2pdf import pisa
from .views import send_message
from django.core.mail import send_mail
from datetime import datetime

from django.db.models import Sum, F, ExpressionWrapper, DecimalField


from django.db.models import F, Sum, FloatField


# from rest_framework.authtoken.models import Token



class DayClosingViewSet(viewsets.ModelViewSet):
    queryset = DayClosing.objects.all()
    serializer_class = DayClosingSerializer

class DayClosingAdminViewSet(viewsets.ModelViewSet):
    queryset = DayClosingAdmin.objects.all()
    serializer_class = DayClosingAdminSerializer

class SaleByStaffServiceViewSet(viewsets.ModelViewSet):
    queryset = SaleByStaffService.objects.all()
    serializer_class = SaleByStaffServiceSerializer

class SaleByStaffItemViewSet(viewsets.ModelViewSet):
    queryset = SaleByStaffItem.objects.all()
    serializer_class = SalesByStaffItemSerializer

class SalesByStaffItemServiceViewSet(viewsets.ModelViewSet):
    queryset = SalesByStaffItemService.objects.all()
    serializer_class = SalesByStaffItemServiceSerializer

class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



class DayClosingListCreateAPIView(APIView):
    def get(self, request,pk, format=None):
        # employee_id = request.session.get('employee_id')
        day_closings = DayClosingAdmin.objects.filter(employee=pk)
        serializer = DayClosingAdminSerializer(day_closings, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
        # employee_id = request.session.get('employee_id')
        employee =get_object_or_404(Employee,id=pk)
        serializer = DayClosingAdminSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.validated_data['status'] = 'pending'
            serializer.validated_data['employee']=employee

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def fetch_total_sale(request,pk,date):
    current_date = date
    # employee_id = request.session.get('employee_id')
    # current_date = timezone.now().strftime('%Y-%m-%d')
    
    total_services = (SalesByStaffItemService.objects
                      .filter(employee_id=pk, date=current_date)
                      .aggregate(total_services=Sum('servicetotal'))['total_services'] or 0) + \
                     (SaleByStaffService.objects
                      .filter(employee_id=pk, date=current_date)
                      .aggregate(total_services=Sum('total_amount'))['total_services'] or 0)

    total_sales = (SalesByStaffItemService.objects
                   .filter(employee_id=pk, date=current_date)
                   .aggregate(total_sales=Sum('itemtotal'))['total_sales'] or 0) + \
                  (SaleByStaffItem.objects
                   .filter(employee_id=pk, date=current_date)
                   .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0) 
  
    total_services_card = (
        SalesByStaffItemService.objects.filter(employee_id=pk, date=current_date,payment_method='card')
        .aggregate(total_services=Sum('servicetotal'))['total_services'] or 0
    )
    total_services_card += (
        SaleByStaffService.objects.filter(employee_id=pk, date=current_date,payment_method='card')
        .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
    )        

    total_sales_card = (
            SalesByStaffItemService.objects.filter(employee_id=pk, date=current_date,payment_method='card')
            .aggregate(total_sales=Sum('itemtotal'))['total_sales'] or 0
        )
    total_sales_card += (
            SaleByStaffItem.objects.filter(employee_id=pk, date=current_date,payment_method='card')
            .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        )

    total_services_cash = (
        SalesByStaffItemService.objects.filter(employee_id=pk, date=current_date,payment_method='cash')
        .aggregate(total_services=Sum('servicetotal'))['total_services'] or 0
    )
    total_services_cash += (
        SaleByStaffService.objects.filter(employee_id=pk, date=current_date,payment_method='cash')
        .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
    )        

    total_sales_cash = (
            SalesByStaffItemService.objects.filter(employee_id=pk, date=current_date,payment_method='cash')
            .aggregate(total_sales=Sum('itemtotal'))['total_sales'] or 0
        )
    total_sales_cash += (
            SaleByStaffItem.objects.filter(employee_id=pk, date=current_date,payment_method='cash')
            .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        )
    
    total_card_collection = total_sales_card + total_services_card
    total_cash_collection = total_sales_cash + total_services_cash


    total_collection = total_sales + total_services 
    
    data = {
        'total_services': float(total_services),
        'total_sales': float(total_sales),
        'total_collection': float(total_collection),
        'total_card_collection': float(total_card_collection),
        'total_cash_collection': float(total_cash_collection),


    }

    return JsonResponse(data)



class DayClosingRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(DayClosingAdmin, pk=pk)

    def get(self, request, pk, format=None):
        day_closing = self.get_object(pk)
        serializer = DayClosingAdminSerializer(day_closing)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        day_closing = self.get_object(pk)
        serializer = DayClosingAdminSerializer(day_closing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        day_closing = self.get_object(pk)
        day_closing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class DayClosingAdminListCreateAPIView(APIView):
    # def get(self, request, pk, format=None):
    #     employee = get_object_or_404(Employee, pk=pk) 
    #     role = Role.objects.filter(name=employee.job_role).first()
    #     if role:
    #         active_modules = role.modules.all()
    #         if active_modules:
    #             day_closing_admins = DayClosingAdmin.objects.filter(employee=pk)
    #             serializer = DayClosingAdminSerializer(day_closing_admins, many=True)
    #             return Response(serializer.data)
    #         else:
    #             return Response({"message": "Admin Day Closing module not enabled for this employee"}, status=status.HTTP_403_FORBIDDEN)
    #     else:
    #         return Response({"message": "No role found for this employee"}, status=status.HTTP_403_FORBIDDEN)


    
    def get(self, request,pk, format=None):
        employee = get_object_or_404(Employee,pk=pk)
        if employee.job_role.modules.filter(url='/dayclosing/admin/').exists():
            day_closing_admins = DayClosingAdmin.objects.filter(employee=pk)
            serializer = DayClosingAdminSerializer(day_closing_admins, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Admin Day Closing module not enabled for this employee"},status=status.HTTP_403_FORBIDDEN)


    def post(self, request,pk, format=None):
        employee =get_object_or_404(Employee,id=pk)
        if employee.job_role.modules.filter(url='/dayclosing/admin/').exists():
            serializer = DayClosingAdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['employee'] = employee
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Admin Day Closing module not enabled for this employee"}, status=status.HTTP_403_FORBIDDEN)



class DayClosingAdminRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(DayClosingAdmin, pk=pk)

    def get(self, request, pk, format=None):
        day_closing_admin = self.get_object(pk)
        serializer = DayClosingAdminSerializer(day_closing_admin)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        day_closing_admin = self.get_object(pk)
        serializer = DayClosingAdminSerializer(day_closing_admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        day_closing_admin = self.get_object(pk)
        day_closing_admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class SaleByStaffServiceListCreateAPIView(APIView):

    def get(self, request,pk, format=None):
        # employee_id = request.session.get('employee_id')
        sales_by_staff_service = SaleByStaffService.objects.filter(employee=pk)
        serializer = SaleByStaffServiceSerializer(sales_by_staff_service, many=True)
        return Response(serializer.data)
    
    def post(self, request,pk, format=None):
        note_list = []
        employee =get_object_or_404(Employee,id=pk)
        serializer = SaleByStaffServiceSerializer(data=request.data)
        if serializer.is_valid():
            # service = serializer.validated_data['service']
            # quantity = serializer.validated_data['quantity']
            # price = serializer.validated_data['price']
            # note_list.append({
            #     "service": service.name,
            #     "quantity": quantity,
            #     "price": float(price), 
            # })
            serializer.validated_data['employee'] = employee
            # serializer.validated_data['note'] = note_list
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # def post(self, request,pk, format=None):
    #     # employee_id = request.session.get('employee_id')
    #     employee =get_object_or_404(Employee,id=pk)
    #     serializer = SaleByStaffServiceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.validated_data['employee']=employee
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleByStaffServiceRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SaleByStaffService, pk=pk)

    def get(self, request, pk, format=None):
        sale_by_staff_service = self.get_object(pk)
        serializer = SaleByStaffServiceSerializer(sale_by_staff_service)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sale_by_staff_service = self.get_object(pk)
        serializer = SaleByStaffServiceSerializer(sale_by_staff_service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sale_by_staff_service = self.get_object(pk)
        sale_by_staff_service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SaleByStaffItemListCreateAPIView(APIView):

    def get(self, request,pk, format=None):
        # employee_id = request.session.get('employee_id')
        sales_by_staff_item = SaleByStaffItem.objects.filter(employee=pk)
        serializer = SalesByStaffItemSerializer(sales_by_staff_item, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
        # employee_id = request.session.get('employee_id')
        # employee =get_object_or_404(Employee,id=pk)
        # serializer = SalesByStaffItemSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data['employee']=employee
        #     serializer.save()
        # note_list = []
        employee = get_object_or_404(Employee,id=pk)
        serializer = SalesByStaffItemSerializer(data=request.data)
        if serializer.is_valid():
            # item = serializer.validated_data['item']
            # quantity = serializer.validated_data['quantity']
            # price = serializer.validated_data['price']
            # note_list.append({
            #     "item": item.name,
            #     "quantity": quantity,
            #     "price": float(price), 
            # })
            serializer.validated_data['employee'] = employee
            # serializer.validated_data['note'] = note_list
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleByStaffItemRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SaleByStaffItem, pk=pk)

    def get(self, request, pk, format=None):
        sale_by_staff_item = self.get_object(pk)
        serializer = SalesByStaffItemSerializer(sale_by_staff_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sale_by_staff_item = self.get_object(pk)
        serializer = SalesByStaffItemSerializer(sale_by_staff_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sale_by_staff_item = self.get_object(pk)
        sale_by_staff_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class SalesByStaffItemServiceListCreateAPIView(APIView):

    def get(self, request, pk,format=None):
        # employee_id = request.session.get('employee_id')
        sales_by_staff_item_service = SalesByStaffItemService.objects.filter(employee=pk)
        serializer = SalesByStaffItemServiceSerializer(sales_by_staff_item_service, many=True)
        return Response(serializer.data)

    def post(self, request, pk,format=None):
        # employee_id = request.session.get('employee_id')
        employee = get_object_or_404(Employee,id=pk)
        serializer = SalesByStaffItemServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['employee']=employee
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesByStaffItemServiceRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SalesByStaffItemService, pk=pk)

    def get(self, request, pk, format=None):
        sale_by_staff_item_service = self.get_object(pk)
        serializer = SalesByStaffItemServiceSerializer(sale_by_staff_item_service)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sale_by_staff_item_service = self.get_object(pk)
        serializer = SalesByStaffItemServiceSerializer(sale_by_staff_item_service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sale_by_staff_item_service = self.get_object(pk)
        sale_by_staff_item_service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Define a serializer for the login form fields
class LoginFormSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

# Modify your view to use the serializer
class EmployeeLoginAPIView(APIView):
    def post(self, request, format=None):
        # Serialize the incoming data using the LoginFormSerializer
        serializer = LoginFormSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Extract the validated data
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')            
            # Check if the username exists in the Employee module
            try:
                employee = Employee.objects.get(username=username,password=password)
                request.session['employee_id'] = employee.id

            except Employee.DoesNotExist:
                return Response({'message': 'Enter valid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # Authenticate the employee
            # employee = authenticate(username=username)
            # print(employee,'kkkkkkkkkk')
            if employee is not None:
                # Generate or retrieve the token for the authenticated employee
                # token, created = Token.objects.get_or_create(user=employee)
                # Get the profile of the authenticated employee
                # employee_profile = get_object_or_404(Employee, username=username)
                
                # Serialize the employee profile
                serializer = EmployeeSerializer(employee)
                
                # Return the serialized data along with token, ID, and username
                response_data = {
                    # 'token': token.key,
                    'id': employee.id,
                    'username': employee.username,
                    **serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # If authentication fails, return unauthorized response
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # If the serializer is not valid, return the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class EmployeeLogoutAPIView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)



class EmployeeDashboardAPIView(APIView):
    def get(self, request,pk ,format=None):
        # Retrieve the employee ID from the session
        # employee_id = request.session.get('employee_id')
        # print(employee_id)
        # Fetch employee details
        employee = get_object_or_404(Employee, id=pk)
        # Fetch associated BusinessProfile for the employee
        business_profile = BusinessProfile.objects.filter(id=employee.business_profile_id).first()
        
        # Fetch associated Shop for the employee
        shop = Shop.objects.filter(name=business_profile.name).first()  
        # Get the current month and year
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Get the first and last day of the current month
        first_day_of_month = timezone.datetime(current_year, current_month, 1)
        last_day_of_month = timezone.datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1])

        # Aggregate total services, total sales, and total advance for the current month
        day_closings = DayClosingAdmin.objects.filter(employee_id=pk, date__gte=first_day_of_month, date__lte=last_day_of_month)
        
        # Check if the employee has a job_role
        if employee and employee.job_role:
            # If job_role exists, filter roles based on it
            role = Role.objects.filter(name=employee.job_role).first()
            # Get active modules based on the filtered role
            active_modules = role.modules.all()
        else:
            active_modules = []
        
        # Check if day_closings is not empty
        if day_closings.exists():
            total_services = day_closings.aggregate(total_services=Sum('total_services'))['total_services'] or 0
            total_sales = day_closings.aggregate(total_sales=Sum('total_sales'))['total_sales'] or 0
            total_advance = day_closings.aggregate(total_advance=Sum('advance'))['total_advance'] or 0
        else:
            # If day_closings is empty, set totals to 0
            total_services = 0
            total_sales = 0
            total_advance = 0
        
        # Commission calculation
        if employee and employee.commission_percentage:
            com_cal = employee.commission_percentage / 100
        else:
            com_cal = 0
        
        # Check if total_services and total_sales are not None
        if total_services is not None and total_sales is not None:
            commission = (total_services + total_sales) * com_cal
        else:
            commission = 0  # Set commission to 0 if total_services or total_sales is None

        # Prepare data for the chart
        chart_data = [{
            'date': closing.date.strftime('%Y-%m-%d'),
            'total_services': float(closing.total_services) if closing.total_services is not None else None,
            'total_sales': float(closing.total_sales) if closing.total_sales is not None else None,
            'advance': float(closing.advance) if closing.advance is not None else None,
        } for closing in day_closings]

        # Convert data to JSON format
        chart_data_json = json.dumps(chart_data)

        #Convert into serialized data
        module_serializer = ModuleSerializer(active_modules, many=True)
        active_modules_data = module_serializer.data  

        # use the below method or EmployeeSerializer
        # employee_data = {
        #     'id': employee.id,
        #     'name': employee.name,
        # }

        # Construct the response
        response_data = {
            'employee':EmployeeSerializer(employee).data,
            'business_profile':BusinessProfileSerializer(business_profile).data,
            'shop': ShopSerializer(shop).data,
            'total_services': total_services,
            'total_sales': total_sales,
            'total_advance': total_advance,
            'commission': commission,
            'chart_data_json': chart_data_json,
            'active_modules': active_modules_data,
        }
        return JsonResponse({"response_data":response_data}, status=status.HTTP_200_OK)
    


class EmployeeProfileAPIView(APIView):
    def get(self, request, pk, format=None):
        employee = get_object_or_404(Employee, id=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class DayClosingReportAPIView(APIView):
    def get(self, request,pk, format=None):
        # logged_in_employee_id = request.session.get('employee_id')  # Retrieve the logged-in employee's ID from the session
        # logged_in_employee_id=1
        day_closings_list = DayClosingAdmin.objects.filter(employee__id=pk).order_by('-created_on')
        # Paginate the day closings list
        paginator = Paginator(day_closings_list, 10)
        page = request.GET.get('page')
        
        try:
            day_closings = paginator.page(page)
        except PageNotAnInteger:
            day_closings = paginator.page(1)
        except EmptyPage:
            day_closings = paginator.page(paginator.num_pages)

        # Convert day closings queryset to JSON
        day_closings_json = [{"date": dc.date, "total_services": dc.total_services, "total_sales": dc.total_sales, "advance":dc.advance,"status":dc.status,"net_collection":dc.net_collection,"total_collection": dc.total_collection} for dc in day_closings]

        return JsonResponse({'day_closings': day_closings_json}, status=status.HTTP_200_OK)


class SalesReportAPIView(APIView):
    def get(self, request,pk, format=None):
        # logged_in_employee_id = request.session.get('employee_id')  # Retrieve the logged-in employee's ID from the session
        # logged_in_employee_id=1

        # Query the sales data filtered by the logged-in employee's ID
        sales = SalesByStaffItemService.objects.filter(employee__id=pk)
        sales_staff_service = SaleByStaffService.objects.filter(employee__id=pk)
        sales_staff_item = SaleByStaffItem.objects.filter(employee__id=pk)

        # Convert sales data to JSON
        sales_json = [{"date": s.date,"product_price":s.pprice,"service_price":s.sprice,"discount":s.discount,"sub_total":s.sub_total,"payment_method":s.payment_method,"product_total":s.itemtotal,"service_total":s.servicetotal,"total_amount": s.total_amount} for s in sales]
        sales_staff_service_json = [{"date": ss.date,"price":ss.price,"discount":ss.discount,"payment_method":ss.payment_method, "total_amount": ss.total_amount} for ss in sales_staff_service]
        sales_staff_item_json = [{"date": si.date, "price":si.price,"discount":si.discount,"payment_method":si.payment_method,"total_amount": si.total_amount} for si in sales_staff_item]

        return JsonResponse({'sales': sales_json, 'sales_staff_service': sales_staff_service_json, 'sales_staff_item': sales_staff_item_json}, status=status.HTTP_200_OK)
    


class ProductListView(APIView):
    def get(self,request,pk):
        employee =get_object_or_404(Employee,pk=pk)
        queryset = Product.objects.filter(business_profile=employee.business_profile_id)
        serializer= ProductSerializer(queryset,many=True)
        return Response(serializer.data)



class ServiceListView(APIView):
    def get(self,request,pk):
        employee = get_object_or_404(Employee,pk=pk)
        queryset = Service.objects.filter(business_profile=employee.business_profile_id)
        serializer = ServiceSerializer(queryset,many=True)
        return Response(serializer.data)



class ProductDetailsView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ServiceDetailsView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class JobRoleApiView(APIView):
    def get(self,request,pk):
        employee = get_object_or_404(Employee,pk=pk)
        queryset = Role.objects.filter(name = employee.job_role.name)
        serializer = JobRoleSerializer(queryset,many=True)
        return Response(serializer.data)

class DailySummaryListCreateAPIView(APIView):
    def get(self, request,pk, format=None):
        employee = get_object_or_404(Employee ,id=pk)
        dailysummarys = DailySummary.objects.filter(business_profile = employee.business_profile_id)
        serializer = DailySummarySerializer(dailysummarys, many=True)
        return Response(serializer.data)

    def post(self, request,pk,format=None):

        employee = get_object_or_404(Employee ,id=pk)
        business_profile_id = employee.business_profile_id
        business_profile = get_object_or_404(BusinessProfile, id=business_profile_id)
        business_license_number =business_profile.license_number
        shop = get_object_or_404(Shop, license_number=business_license_number)

        serializer = DailySummarySerializer(data=request.data)
        if serializer.is_valid():
            daily_summary = serializer.save() 

            msg_parts = []
            if daily_summary.opening_balance != 0:
                msg_parts.append(f"Opening: {daily_summary.opening_balance}")
            if daily_summary.total_received_amount != 0:
                msg_parts.append(f"Collection: {daily_summary.total_received_amount}")
            if daily_summary.total_expense_amount != 0:
                msg_parts.append(f"Expense: {daily_summary.total_expense_amount}")
            if daily_summary.total_bank_deposit != 0:
                msg_parts.append(f"Bank: {daily_summary.total_bank_deposit}")
            if daily_summary.balance != 0:
                msg_parts.append(f"Closing: {daily_summary.balance}")
            
            msg = "\n".join(msg_parts)
            # sms
            send_message(request, msg)
            # email 
            subject = "Daily Summary"
            message = msg
            to_email = shop.admin_email
            cc_emails = ['navas@mitesolutions.com']
            send_mail(subject, message, None, [to_email], cc_emails)

            # msg = f"Payments: {daily_summary.total_expense_amount}\nBanking: {daily_summary.total_bank_deposit}\nClosing: {daily_summary.balance}"
            # send_message(request,msg)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailySummaryRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(DailySummary, pk=pk)

    def get(self, request, pk, format=None):
        daily_summary = self.get_object(pk)
        serializer = DailySummarySerializer(daily_summary)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        daily_summary = self.get_object(pk)
        serializer = DailySummarySerializer(daily_summary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        day_closing = self.get_object(pk)
        day_closing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# class FetchDailySummary(APIView):

#     def get(self,request,pk, date):
#         opening_balance = 0
#         total_received_amount = 0
#         total_expense_amount = 0
#         total_bank_deposit = 0
#         net_collection = 0
#         balance = 0

#         employee = get_object_or_404(Employee, id=pk)        
#         business_profile = get_object_or_404(BusinessProfile, id=employee.business_profile_id)
#         try:
#             daily_summary = DailySummary.objects.filter(date=date).latest('created_on')
#             opening_balance = daily_summary.opening_balance
#         except DailySummary.DoesNotExist:
#             data = {
#             'opening_balance': opening_balance,
#             'net_collection': net_collection,
#             'total_received_amount': total_received_amount,
#             'total_expense_amount': total_expense_amount,
#             'total_bank_deposit': total_bank_deposit,
#             'balance': balance,
#             'msg':'Please add daily summary'
#             }
#             return Response(data)

#         day_closing_admins = DayClosingAdmin.objects.filter(date=date)

class FetchDailySummary(APIView):

    def get(self,request,pk, date):
        opening_balance = 0
        total_received_amount = 0
        total_expense_amount = 0
        total_bank_deposit = 0
        net_collection = 0
        balance = 0
        total_advance = 0

        employee = get_object_or_404(Employee, id=pk)

        business_profile = get_object_or_404(BusinessProfile, id=employee.business_profile_id)
        employees = Employee.objects.filter(business_profile_id = business_profile.id)
        # 
        if DailySummary.objects.filter(business_profile = business_profile.id).exists():
            last_daliy_summary_date = DailySummary.objects.filter(business_profile = business_profile.id).order_by('-date').first()
            yesterday_date = last_daliy_summary_date.date
        else:
            yesterday_date = datetime.now().date()
        # try:
        #     daily_summary = DailySummary.objects.filter(business_profile = business_profile.id).latest('created_on')
        #     opening_balance = daily_summary.balance
        # except DailySummary.DoesNotExist:
        #     pass
        try:
            daily_summary = DailySummary.objects.get(business_profile = business_profile.id, date=yesterday_date)
            opening_balance = daily_summary.balance
        except DailySummary.DoesNotExist:
            pass
        
        try:
            day_closing_admin = DayClosingAdmin.objects.filter(date=date, business_profile=business_profile.id,status="approved").latest('created_on')
            net_collection = day_closing_admin.net_collection
            total_advance = day_closing_admin.advance
        except DayClosingAdmin.DoesNotExist:
            data = {
                'opening_balance': opening_balance,
                'net_collection': net_collection,
                'total_received_amount': total_received_amount,
                'total_expense_amount': total_expense_amount,
                'total_bank_deposit': total_bank_deposit,
                'balance': opening_balance + total_received_amount- total_expense_amount - total_bank_deposit,
                'business_profile':business_profile.id,
                'advance':total_advance,
                'msg': 'DayClosingAdmin matching query does not exist',
            }
            return Response(data)
        
        selected_date = date
        total_services = (
        SaleByAdminService.objects.filter(date=selected_date, employee__business_profile_id=business_profile.id,payment_method='card')
        .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
        )

        total_services += (
            SalesByStaffItemService.objects.filter(date=selected_date,employee__business_profile_id=business_profile.id,payment_method='card')
            .aggregate(total_services=Sum('servicetotal'))['total_services'] or 0
        )
        total_services += (
            SaleByStaffService.objects.filter(date=selected_date,employee__business_profile_id=business_profile.id,payment_method='card')
            .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
        )
        # Fetch total sales for the selected date and employee
        total_sales = (
            SalesByAdminItem.objects.filter(date=selected_date,employee__business_profile_id=business_profile.id,payment_method='card')
            .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        )
        total_sales += (
            SalesByStaffItemService.objects.filter(date=selected_date,employee__business_profile_id=business_profile.id,payment_method='card')
            .aggregate(total_sales=Sum('itemtotal'))['total_sales'] or 0
        )
        total_sales += (
            SaleByStaffItem.objects.filter(date=selected_date,employee__business_profile_id=business_profile.id,payment_method='card')
            .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        )
        # Calculate total collection
        # total_collection = total_sales + total_services
        total_card_collection = total_sales + total_services



        # Fetch the DayClosingAdmin objects for the given date
        # day_closing_admins = DayClosingAdmin.objects.filter(date = date, business_profile = business_profile.id,employee=employee.id)
        # if day_closing_admins.exists():
        
        # day_closing_admin = day_closing_admins.latest('created_on')
        # net_collection = day_closing_admin.net_collection

        day_closing_admin_net_collection = DayClosingAdmin.objects.filter(date = date, business_profile = business_profile.id, employee__in = employees,status="approved").aggregate(total_amount=Sum('total_collection'))['total_amount'] or 0
        total_advance = DayClosingAdmin.objects.filter(date = date, business_profile = business_profile.id, employee__in = employees,status="approved").aggregate(total_advance=Sum('advance'))['total_advance'] or 0



        # Calculate total_received_amount from ReceiptTransactions
        receipt_transactions_total = ReceiptTransaction.objects.filter(date=date, business_profile = business_profile.id).aggregate(total_amount=Sum('received_amount'))['total_amount'] or 0
        # total_received_amount = receipt_transactions_total + net_collection
        total_received_amount= (receipt_transactions_total + day_closing_admin_net_collection) 


        # Calculate total_bank_deposit from BankDeposit
        bank_deposit = BankDeposit.objects.filter(date=date, business_profile=business_profile.id).aggregate(amount=Sum('amount'))['amount'] or 0
        total_bank_deposit = bank_deposit + total_card_collection

        # Calculate total_expense_amount from PaymentTransactions
        payment_transactions_total = PaymentTransaction.objects.filter(date=date, business_profile = business_profile.id).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_expense_amount = payment_transactions_total

        # Calculate the balance
        balance = (opening_balance + total_received_amount ) - (total_expense_amount + total_advance)
        balance = balance - total_bank_deposit

        # Construct data dictionary
        data = {
            'opening_balance': opening_balance,
            'net_collection': day_closing_admin_net_collection,
            'total_received_amount': total_received_amount,
            'total_expense_amount': total_expense_amount,
            'total_bank_deposit': total_bank_deposit,
            'balance': balance,
            'total_card_sale': total_sales,
            'total_card_service': total_services,
            'business_profile':business_profile.id,
            'advance':total_advance,
            'msg': 'Day closing available',
            # 'employee':employee.first_name,
        }

        return JsonResponse(data)

# class FetchDailySummary(APIView):

#     def get(self, request, pk, date):
#         opening_balance = 0
#         total_received_amount = 0
#         total_expense_amount = 0
#         total_bank_deposit = 0
#         net_collection = 0
#         balance = 0
#         advance = 0

#         employee = get_object_or_404(Employee, id=pk)
#         business_profile = get_object_or_404(BusinessProfile, id=employee.business_profile_id)
#         employees = Employee.objects.filter(business_profile_id=business_profile.id)

#         # Check if any employee has a pending day closing
#         staff_service_transactions = SaleByStaffService.objects.filter(date=date, employee__business_profile_id=business_profile.id).values_list('employee_id', flat=True)
#         staff_item_transactions = SaleByStaffItem.objects.filter(date=date, employee__business_profile_id=business_profile.id).values_list('employee_id', flat=True)
#         admin_service_transactions = SaleByAdminService.objects.filter(date=date, employee__business_profile_id=business_profile.id).values_list('employee_id', flat=True)
#         admin_item_transactions = SalesByAdminItem.objects.filter(date=date, employee__business_profile_id=business_profile.id).values_list('employee_id', flat=True)
#         staff_item_service_transactions = SalesByStaffItemService.objects.filter(date=date, employee__business_profile_id=business_profile.id).values_list('employee_id', flat=True)

#         all_employee_ids = set(staff_service_transactions) | set(staff_item_transactions) | set(admin_service_transactions) | set(admin_item_transactions) | set(staff_item_service_transactions)

#         employees_with_transactions = Employee.objects.filter(id__in=all_employee_ids, business_profile_id=business_profile.id)

#         for emp in employees_with_transactions:
#             day_closing_completed = DayClosingAdmin.objects.filter(employee_id=emp.id, date=date, business_profile=business_profile.id).exists()
#             if not day_closing_completed:
#                 response_data = [{
#                     'id': emp.id,
#                     'first_name': emp.first_name,
#                     'second_name': emp.second_name,
#                     'msg': 'Day closing pending for employee'
#                 }]
#                 return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST, safe=False)

#         # Proceed with daily summary calculation if all employees have completed day closing
#         try:
#             daily_summary = DailySummary.objects.filter(business_profile=business_profile.id).latest('created_on')
#             opening_balance = daily_summary.balance
#         except DailySummary.DoesNotExist:
#             pass

#         try:
#             day_closing_admin = DayClosingAdmin.objects.filter(date=date, business_profile=business_profile.id, status="approved").latest('created_on')
#             net_collection = day_closing_admin.net_collection
#             advance = day_closing_admin.advance
#         except DayClosingAdmin.DoesNotExist:
#             data = {
#                 'opening_balance': opening_balance,
#                 'net_collection': net_collection,
#                 'total_received_amount': total_received_amount,
#                 'total_expense_amount': total_expense_amount,
#                 'total_bank_deposit': total_bank_deposit,
#                 'balance': opening_balance + total_received_amount - total_expense_amount - total_bank_deposit,
#                 'business_profile': business_profile.id,
#                 'advance': advance,
#                 'msg': 'DayClosingAdmin matching query does not exist',
#             }
#             return Response(data, status=status.HTTP_200_OK)

#         selected_date = date
#         total_services = (
#             SaleByAdminService.objects.filter(date=selected_date, employee__business_profile_id=business_profile.id, payment_method='card')
#             .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
#         )
#         total_services += (
#             SalesByStaffItemService.objects.filter(date=selected_date, employee__business_profile_id=business_profile.id, payment_method='card')
#             .aggregate(total_services=Sum('servicetotal'))['total_services'] or 0
#         )
#         total_services += (
#             SaleByStaffService.objects.filter(date=selected_date, employee__business_profile_id=business_profile.id, payment_method='card')
#             .aggregate(total_services=Sum('total_amount'))['total_services'] or 0
#         )

#         total_sales = (
#             SalesByAdminItem.objects.filter(date=selected_date, employee__business_profile_id=business_profile.id, payment_method='card')
#             .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
#         )
#         total_sales += (
#             SalesByStaffItemService.objects.filter(date=selected_date, employee__business_profile_id=business_profile.id, payment_method='card')
#             .aggregate(total_sales=Sum('itemtotal'))['total_sales'] or 0
#         )
#         total_sales += (
#             SaleByStaffItem.objects.filter(date=selected_date, employee__business_profile_id=business_profile.id, payment_method='card')
#             .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
#         )

#         total_card_collection = total_sales + total_services

#         day_closing_admin_net_collection = DayClosingAdmin.objects.filter(date=date, business_profile=business_profile.id, employee__in=employees, status="approved").aggregate(total_amount=Sum('net_collection'))['total_amount'] or 0
#         total_advance = DayClosingAdmin.objects.filter(date=date, business_profile=business_profile.id, employee__in=employees, status="approved").aggregate(total_advance=Sum('advance'))['total_advance'] or 0

#         receipt_transactions_total = ReceiptTransaction.objects.filter(date=date, business_profile=business_profile.id).aggregate(total_amount=Sum('received_amount'))['total_amount'] or 0
#         total_received_amount = receipt_transactions_total + day_closing_admin_net_collection

#         bank_deposit = BankDeposit.objects.filter(date=date, business_profile=business_profile.id).aggregate(amount=Sum('amount'))['amount'] or 0
#         total_bank_deposit = bank_deposit + total_card_collection

#         payment_transactions_total = PaymentTransaction.objects.filter(date=date, business_profile=business_profile.id).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
#         total_expense_amount = payment_transactions_total

#         balance = (opening_balance + total_received_amount) - total_expense_amount - total_bank_deposit

#         data = {
#             'opening_balance': opening_balance,
#             'net_collection': day_closing_admin_net_collection,
#             'total_received_amount': total_received_amount,
#             'total_expense_amount': total_expense_amount,
#             'total_bank_deposit': total_bank_deposit,
#             'balance': balance,
#             'total_card_sale': total_sales,
#             'total_card_service': total_services,
#             'business_profile': business_profile.id,
#             'advance': total_advance,
#             'msg': 'Day closing available',
#         }

#         return JsonResponse(data, status=status.HTTP_200_OK)

                
        #     # day_closing_admins = DayClosingAdmin.objects.filter(date = date, business_profile = business_profile.id)
        
        # # day_closing_admin = day_closing_admins.latest('created_on')
        # # net_collection = day_closing_admin.net_collection

        # # Calculate total_received_amount from ReceiptTransactions
        # receipt_transactions_total = ReceiptTransaction.objects.filter(date=date, business_profile = business_profile.id).aggregate(total_amount=Sum('received_amount'))['total_amount'] or 0
        # total_received_amount = receipt_transactions_total + net_collection

        # # Calculate total_bank_deposit from BankDeposit
        # total_bank_deposit = BankDeposit.objects.filter(date=date, business_profile=business_profile.id).aggregate(amount=Sum('amount'))['amount'] or 0

        # # Calculate total_expense_amount from PaymentTransactions
        # payment_transactions_total = PaymentTransaction.objects.filter(date=date, business_profile = business_profile.id).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        # total_expense_amount = payment_transactions_total

        # # Calculate the balance
        # balance = opening_balance + total_received_amount - total_expense_amount - total_bank_deposit

        # data = {
        #     'opening_balance': opening_balance,
        #     'net_collection': net_collection,
        #     'total_received_amount': total_received_amount,
        #     'total_expense_amount': total_expense_amount,
        #     'total_bank_deposit': total_bank_deposit,
        #     'balance': balance
        #     }
        # return Response(data)

    



from django.template.loader import get_template
from xhtml2pdf import pisa

class GenerateInvoicePDF(APIView):
    def get(self, request, id, type):
        invoice_instance = None
        if type == 'salebyadminservice':
            invoice_instance = get_object_or_404(SaleByAdminService, id=id)
            invoice_id = f"INV_SAS_{invoice_instance.pk}"
            data_source = "Admin"
        elif type == 'salebyadminproduct':
            invoice_instance = get_object_or_404(SalesByAdminItem, id=id)
            invoice_id = f"INV_SAP_{invoice_instance.pk}"
            data_source = "Admin"
        elif type == 'salesbystaffitemservice':
            invoice_instance = get_object_or_404(SalesByStaffItemService, id=id)
            invoice_id = f"INV_SSPS_{invoice_instance.pk}"
            data_source = "Staff"
        elif type == 'salebystaffitem':
            invoice_instance = get_object_or_404(SaleByStaffItem, id=id)
            invoice_id = f"INV_SSP_{invoice_instance.pk}"
            data_source = "Staff"
        elif type == 'salebystaffservice':
            invoice_instance = get_object_or_404(SaleByStaffService, id=id)
            invoice_id = f"INV_SSS_{invoice_instance.pk}"
            data_source = "Staff"
        else:
            return Response({"error": "Invalid invoice type"}, status=400)

        if invoice_instance is None:
            return Response({"error": "Invoice not found"}, status=404)

        business_profile = get_object_or_404(BusinessProfile, id=invoice_instance.employee.business_profile_id)
        vat = business_profile.vat_percentage
        if invoice_instance.note:
            note_str = invoice_instance.note
            note_list = eval(note_str)
            invoice_details = []

            for item in note_list:
                note = item.get('service') or item.get('product')
                quantity = item['quantity']
                price = item['price']

                invoice_details.append({
                    'note': note,
                    'quantity': quantity,
                    'price': price,
                })
        else:
            invoice_details = []

        invoice = {
            'id': invoice_id,
            'date': invoice_instance.date,
            'employee': invoice_instance.employee,
            'payment_method': invoice_instance.payment_method,
            'total_amount': invoice_instance.total_amount,
            'details': invoice_details,
            'discount': invoice_instance.discount,
            'data_source': data_source,
            'VAT': vat
        }
        template_path = 'preview_invoice.html'
        template = get_template(template_path)
        html = template.render(invoice)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{id}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return Response({'error': 'PDF creation error'}, status=500)
        return response

class InvoiceDetailsAPIView(APIView):
    def get(self, request, id, type):

        invoice_instance =None
        sub_total = 0

        if type == 'salesbystaffitemservice':
            invoice_instance = get_object_or_404(SalesByStaffItemService, id=id)
            invoice_id = f"INV_SSPS_{invoice_instance.pk}"
            data_source = "Staff"
            sub_total = invoice_instance.sub_total

        elif type == 'salesbystaffitem':
            invoice_instance = get_object_or_404(SaleByStaffItem, id=id)
            invoice_id = f"INV_SSP_{invoice_instance.pk}"
            data_source = "Staff"
            sub_total = (invoice_instance.total_amount) + (invoice_instance.discount)

        elif type == 'salesbystaffservice':
            invoice_instance = get_object_or_404(SaleByStaffService, id=id)
            invoice_id = f"INV_SSS_{invoice_instance.pk}"
            data_source = "Staff"
            sub_total = (invoice_instance.total_amount) + (invoice_instance.discount)

        else:
            return Response({"error": "Invalid invoice type"}, status=400)

        if invoice_instance is None:
            return Response({"error": "Invoice not found"}, status=404)


        business_profile = get_object_or_404(BusinessProfile ,id=invoice_instance.employee.business_profile_id) 
        vat = business_profile.vat_percentage
        if invoice_instance.note:
            note_str = invoice_instance.note
            note_list = eval(note_str)
            invoice_details = []

            for item in note_list:
                note = ""
                if 'service' in item: 
                    note = item['service']
                elif 'product' in item: 
                    note = item['product']
                elif 'service' in item and 'product' in item:
                    note = item['product']
                    note = item['service']
                else:
                    pass
                quantity = item['quantity']
                price = item['price']

                invoice_details.append({
                    'note': note,
                    'quantity': quantity,
                    'price': price,
                    'total':price*quantity
                })
        else:
            invoice_details = []

        invoice = {
            'id': invoice_id,
            'date': invoice_instance.date,
            'employee': invoice_instance.employee,
            'payment_method': invoice_instance.payment_method,
            'total_amount': invoice_instance.total_amount,
            'details': invoice_details,
            'discount':invoice_instance.discount,
            'data_source': data_source,
            'VAT' :vat,
            'sub_total':sub_total
        }
        template_path = 'preview_invoice.html'
        template = get_template(template_path)
        html = template.render(invoice)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{id}.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


class DayClosingPendingEmployeeList(APIView):
    def get(self, request, business_id, date):
        try:
            business_profile = BusinessProfile.objects.get(id=business_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        pending_day_closings = DayClosingAdmin.objects.filter(status='pending', date=date)
        # Get the set of employee IDs associated with these day closings and the given business profile ID
        employee_ids = pending_day_closings.filter(employee__business_profile_id=business_profile.id).values_list('employee', flat=True).distinct()
        # Query the Employee model for these employees
        employees = Employee.objects.filter(id__in=employee_ids)
        # Serialize the employee data
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def get(self, request,business_profile_id, date):
    #     all_employees = Employee.objects.filter(business_profile_id = business_profile_id)
    #     employees_not_completed = []
    #     for employee in all_employees:
    #         if not DayClosingAdmin.objects.filter(date=date, employee=employee).exists():
    #             employees_not_completed.append(employee)
        
    #     # Serialize the list of employees
    #     serializer = EmployeeSerializer(employees_not_completed, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)




class BusinessProfileApiView(APIView):

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        business_id = employee.business_profile_id

        try:
            business = BusinessProfile.objects.get(id=business_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BusinessProfileDetailsSerilaizer(business)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllEmployeeListApiView(APIView):
    def get(self, request, business_profile_id):
        employees = Employee.objects.filter(business_profile_id=business_profile_id)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

# class SalesReportPdfApiView(APIView):
#     def get(self, request, employee_id, year, month):
#         # Filter sales for the given employee and month
#         sales = DayClosingAdmin.objects.filter(
#             employee=employee_id,
#             date__year=year,
#             date__month=month
#         )
#         # transactions = sales.values('date').annotate(total_collection=Sum('total_amount'))
#         transactions = sales.values('date','total_services','total_sales','total_collection','advance','employee__commission_percentage').annotate(
#         total_collection_with_commission=ExpressionWrapper(
#         F('total_collection') * (F('employee__commission_percentage') / 100.0),
#         output_field=FloatField()
#          ) )
#         return Response(transactions)

from django.db.models import F, Sum, FloatField
from decimal import Decimal
from django.db.models.functions import Coalesce


class SalesReportPdfApiView(APIView):
    def get(self, request, employee_id, year, month):
        # Filter sales for the given employee and month
        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        sales = DayClosingAdmin.objects.filter(
            employee=employee_id,
            date__year=year,
            date__month=month
        )
        transactions = sales.values('date', 'total_services', 'total_sales', 'total_collection', 'advance','employee__commission_percentage').annotate(
        total_collection_with_commission=ExpressionWrapper(
            F('total_collection') * (Coalesce(F('employee__commission_percentage'), 0) / 100.0),
            output_field=DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as needed
        ),
    )

        
 
        # transactions = sales.values('date').annotate(total_collection=Sum('total_amount'))
        # transactions = sales.values('date','total_services','total_sales','total_collection','advance','employee__commission_percentage').annotate(
        # total_collection_with_commission=ExpressionWrapper(
        # F('total_collection') * (F('employee__commission_percentage') / 100.0),
        # output_field=FloatField()
        #  ) )
        # transactions = sales.values('date', 'total_services', 'total_sales', 'total_collection', 'advance').annotate(
        # total_collection_with_commission=ExpressionWrapper(
        #     F('total_collection') * (F('employee__commission_percentage') / 100.0),
        #     output_field=DecimalField()
        # ),
        # )
        totals = sales.aggregate(
            advance_sum=Sum('advance'),
            total_commission_sum=Sum(
                ExpressionWrapper(
                    F('total_collection') * (Coalesce(F('employee__commission_percentage'), 0) / 100.0),
                    output_field=DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as needed
                )
            )
        )
        advance_sum = totals.get('advance_sum', Decimal(0)) or Decimal(0)
        total_commission_sum = totals.get('total_commission_sum', 0.0) or 0.0

        # # Employee allowances
        basic_pay = Decimal(employee.basic_pay or 0)
        house_allowance = Decimal(employee.house_allowance or 0)
        transportation_allowance = Decimal(employee.transportation_allowance or 0)
        total_commission_sum = Decimal(total_commission_sum)
        advance_sum = Decimal(advance_sum)

        # Calculate total salary
        # total_salary = basic_pay + house_allowance + transportation_allowance + total_commission_sum - advance_sum


        response_data = {
            "employee": {
                "basic_pay": employee.basic_pay,
                "house_allowance": employee.house_allowance,
                "transportation_allowance": employee.transportation_allowance,
                "total_commission_sum": totals['total_commission_sum'],
                "total_advance_sum": totals['advance_sum'],
                # "total_salary":total_salary
            },
            "transactions": list(transactions),
        }

        return Response(response_data)


class LastDayClosingDateView(APIView):
    def get(self, request, employee_id, *args, **kwargs):
        try:
            # Fetch the employee object
            employee = get_object_or_404(Employee, id=employee_id)
            business_profile_id = employee.business_profile_id

            # Fetch the latest day closing for the business profile
            last_day_closing = DayClosingAdmin.objects.filter(
                employee__id = employee.id,
                employee__business_profile_id=business_profile_id
            # ).latest('date')
            ).order_by('-date').first()

            # Return the date of the last day closing
            return Response({"date": last_day_closing.date}, status=status.HTTP_200_OK)
        
        except DayClosingAdmin.DoesNotExist:
            # Handle the case where no day closing record is found
            return Response(
                {"error": "No day closing found for the employee's business profile"},
                status=status.HTTP_404_NOT_FOUND
            )

class LastDaliySummaryDateView(APIView):
    def get(self, request, employee_id, *args, **kwargs):
        try:
            # Fetch the employee object
            employee = get_object_or_404(Employee, id=employee_id)
            business_profile_id = employee.business_profile_id

            # Fetch the latest day closing for the business profile
            last_day_summary = DailySummary.objects.filter(
                business_profile=business_profile_id
            ).latest('date')

            # Return the date of the last day closing
            return Response({"date": last_day_summary.date}, status=status.HTTP_200_OK)
        
        except DailySummary.DoesNotExist:
            # Handle the case where no day closing record is found
            return Response(
                {"error": "No daily summary found for the business profile"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class SalesReportPdfAPIView(APIView):
    def get(self, request, pk, start_date, end_date, format=None):
        # Convert start_date and end_date from strings to date objects
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Filter the sales reports by employee and date range
        sales_item_service = SalesByStaffItemService.objects.filter(
            employee_id=pk,
            date__range=(start_date, end_date)
        )
        sales_service = SaleByStaffService.objects.filter(employee__id=pk,
        date__range=(start_date, end_date)
        )
        sales_item = SaleByStaffItem.objects.filter(employee__id=pk,
        date__range=(start_date, end_date)
        )

        total_discount = 0
        total_sub_total = 0
        total_amount = 0

        sales_json = []
        
       
        for sales in sales_item_service:
            sub_total = sales.sub_total
            total_discount += sales.discount
            total_sub_total += sub_total
            total_amount += sales.total_amount

            report_data = {
                'date': sales.date,
                'discount': sales.discount,
                'sub_total': sales.sub_total,
                'payment_method': sales.payment_method,
                'product_total': sales.itemtotal,
                'service_total': sales.servicetotal,
                'total_amount': sales.total_amount,
            }
            sales_json.append(report_data)
        
        for sales in sales_service:
            sub_total = sales.quantity * sales.price
            total_discount += sales.discount
            total_sub_total += sub_total
            total_amount += sales.total_amount

            report_data = {
                'date': sales.date,
                'discount': sales.discount,
                'sub_total': sales.quantity*sales.price,
                'payment_method': sales.payment_method,
                'product_total': "-", 
                'service_total': sales.quantity*sales.price,
                'total_amount': sales.total_amount,
            }
            sales_json.append(report_data)
        
        for sales in sales_item:
            sub_total = sales.quantity * sales.price
            total_discount += sales.discount
            total_sub_total += sub_total
            total_amount += sales.total_amount

            report_data = {
                'date': sales.date,
                'discount': sales.discount,
                'sub_total': sales.quantity*sales.price,
                'payment_method': sales.payment_method,
                'product_total': sales.quantity*sales.price,
                'service_total': "-",  
                'total_amount': sales.total_amount,
            }
            sales_json.append(report_data)

        
        # Render the template with the report data
        template_path = 'sales_report_pdf.html'
        context = {
            'details': sales_json,
            'total_discount': total_discount,
            'total_sub_total': total_sub_total,
            'total_amount': total_amount,

        }
        template = get_template(template_path)
        html = template.render(context)  # Pass the context as a dictionary
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Ezshop sales report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

class DayClosingReportPdfAPIView(APIView):

    def get(self,request,pk,start_date,end_date):

        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        day_closings_list = DayClosingAdmin.objects.filter(employee__id=pk,date__range=(start_date, end_date))
        
        day_closings_json = [{"date": dc.date, "total_services": dc.total_services, "total_sales": dc.total_sales, "advance":dc.advance,"status":dc.status,"net_collection":dc.net_collection,"total_collection": dc.total_collection} for dc in day_closings_list]

        template_path = 'day_closing_report_pdf.html'
        context = {
            'details': day_closings_json,
        }
        template = get_template(template_path)
        html = template.render(context)  # Pass the context as a dictionary
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Ezshop day closing report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class DailySummaryReportPdfAPIView(APIView):

    def get(self,request,pk,start_date,end_date):
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        try:
            employee = Employee.objects.get(pk=pk)
        except ObjectDoesNotExist:
            employee = None
            return JsonResponse({"error":f"No employee found with primary key {pk}."})
        except MultipleObjectsReturned:
            employee = None
            print(f"Multiple employees found with primary key {pk}.")
            return JsonResponse({"error":f"Multiple employees found with primary key {pk}."})
        except Exception as e:
            employee = None
            print(f"An unexpected error occurred: {e}")
            return JsonResponse({"error":f"An unexpected error occurred {e}."})
        business_profile = employee.business_profile_id
        daily_summary_list = DailySummary.objects.filter(business_profile=business_profile,date__range=(start_date, end_date))
        daily_summary = [{"date": ds.date, "opening_balance": ds.opening_balance, "total_received_amount": ds.total_received_amount, "total_expense_amount":ds.total_expense_amount,"total_bank_deposit":ds.total_bank_deposit,"balance":ds.balance,"advance":ds.advance} for ds in daily_summary_list]
        template_path = 'daily_summary_report_pdf.html'
        context = {
            'details': daily_summary,
        }
        template = get_template(template_path)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Ezshop daily summary report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response



class CommissionReportAPIViewPdf(APIView):
    def get(self, request, employee_id, start_date,end_date):
        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        sales = DayClosingAdmin.objects.filter(
            employee=employee_id,
            # date__year=year,
            # date__month=month
            date__range=(start_date, end_date)

        )
        transactions = sales.values('date', 'total_services', 'total_sales', 'total_collection', 'advance','employee__commission_percentage').annotate(
        total_collection_with_commission=ExpressionWrapper(
            F('total_collection') * (Coalesce(F('employee__commission_percentage'), 0) / 100.0),
            output_field=DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as needed
        ),
        )
        totals = sales.aggregate(
            service_sum = Sum('total_services'),
            sales_sum = Sum('total_sales'),
            collection_sum = Sum('total_collection'),
            advance_sum=Sum('advance'),
            total_commission_sum=Sum(
                ExpressionWrapper(
                    F('total_collection') * (Coalesce(F('employee__commission_percentage'), 0) / 100.0),
                    output_field=DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as needed
                )
            )
        )
        advance_sum = totals.get('advance_sum', Decimal(0)) or Decimal(0)
        total_commission_sum = totals.get('total_commission_sum', 0.0) or 0.0

        basic_pay = Decimal(employee.basic_pay or 0)
        house_allowance = Decimal(employee.house_allowance or 0)
        transportation_allowance = Decimal(employee.transportation_allowance or 0)
        total_commission_sum = Decimal(total_commission_sum)
        advance_sum = Decimal(advance_sum)

        response_data = {
                "employee_name":employee.username,
                "basic_pay": employee.basic_pay,
                "house_allowance": employee.house_allowance,
                "transportation_allowance": employee.transportation_allowance,
                "total_commission_sum": totals['total_commission_sum'],
                "total_advance_sum": totals['advance_sum'],
                "total_service_sum": totals['service_sum'],
                "total_sales_sum": totals['sales_sum'],
                "total_collection_sum": totals['collection_sum'],
                "balance":totals["total_commission_sum"] - totals['advance_sum']


        }
        template_path = 'commission_report_pdf.html'
        context = {
            'details': transactions,
            'employee_data':response_data
        }
        template = get_template(template_path)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Ezshop Commission report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response



        # return Response({'context':context})

class ExpenseTypeListCreateAPIView(APIView):

    def get(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        expense_types = ExpenseType.objects.filter(business_profile=business_profile_id)
        serializer = ExpenseTypeSerializer(expense_types, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request,business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        serializer = ExpenseTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['business_profile'] = business_profile.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ExpenseTypeRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(ExpenseType, pk=pk)

    def get(self, request, pk, format=None):
        expense = self.get_object(pk)
        serializer = ExpenseTypeSerializer(expense)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        expense = self.get_object(pk)
        serializer = ExpenseTypeSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        expense = self.get_object(pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReceiptTypeListCreateAPIView(APIView):
    def get(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        receipt_types = ReceiptType.objects.filter(business_profile=business_profile_id)
        serializer = ReceiptTypeSerializer(receipt_types, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request,business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        serializer = ReceiptTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['business_profile'] = business_profile.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReceiptTypeRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(ReceiptType, pk=pk)

    def get(self, request, pk, format=None):
        receipt = self.get_object(pk)
        serializer = ReceiptTypeSerializer(receipt)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        receipt = self.get_object(pk)
        serializer = ReceiptTypeSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        receipt = self.get_object(pk)
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseTransactionListCreateAPIView(APIView):

    def get(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        payments = PaymentTransaction.objects.filter(business_profile=business_profile_id)
        serializer = PaymentTransactionSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        
        if isinstance(request.data, list):
            serializer = PaymentTransactionSerializer(data=request.data, many=True)
        else:
            serializer = PaymentTransactionSerializer(data=[request.data], many=True)

        if serializer.is_valid():
            for item in serializer.validated_data:
                item['business_profile'] = business_profile.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseTransactionRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(PaymentTransaction, pk=pk)

    def get(self, request, pk, format=None):
        expense = self.get_object(pk)
        serializer = PaymentTransactionSerializer(expense)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        expense = self.get_object(pk)
        serializer = PaymentTransactionSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        expense = self.get_object(pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReceiptTransactionListCreateAPIView(APIView):

    def get(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        receipts = ReceiptTransaction.objects.filter(business_profile=business_profile_id)
        serializer = ReceiptTransactionSerializer(receipts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)

        if isinstance(request.data, list):
            serializer = ReceiptTransactionSerializer(data=request.data, many=True)
        else:
            serializer = ReceiptTransactionSerializer(data=[request.data], many=True)

        if serializer.is_valid():
            for item in serializer.validated_data:
                item['business_profile'] = business_profile.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReceiptTransactionRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(ReceiptTransaction, pk=pk)

    def get(self, request, pk, format=None):
        receipt = self.get_object(pk)
        serializer = ReceiptTransactionSerializer(receipt)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        receipt = self.get_object(pk)
        serializer = ReceiptTransactionSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        receipt = self.get_object(pk)
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BankDepositTransactionListCreateAPIView(APIView):

    def get(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        banks = BankDeposit.objects.filter(business_profile=business_profile_id)
        serializer = BankDepositSerializer(banks, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request,business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        
        serializer = BankDepositSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['business_profile'] = business_profile.id
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BankDepositRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(BankDeposit, pk=pk)

    def get(self, request, pk, format=None):
        bank = self.get_object(pk)
        serializer = BankDepositSerializer(bank)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        bank = self.get_object(pk)
        serializer = BankDepositSerializer(bank, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        bank = self.get_object(pk)
        bank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BankListAPIView(APIView):
    def get(self, request, business_profile_id, format=None):
        try:
            business_profile = BusinessProfile.objects.get(pk=business_profile_id)
        except BusinessProfile.DoesNotExist:
            return Response({"error": "Business profile not found"}, status=404)
        banks = Bank.objects.filter(business_profile=business_profile_id)
        serializer = BankSerializer(banks, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


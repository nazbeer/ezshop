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
    def get(self, request, format=None):
        employee_id = request.session.get('employee_id')
        day_closings = DayClosing.objects.filter(employee=employee_id)
        serializer = DayClosingSerializer(day_closings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        employee_id = request.session.get('employee_id')
        employee =get_object_or_404(Employee,id=employee_id)
        serializer = DayClosingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['employee']=employee
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def fetch_total_sale(request):
    employee_id = request.session.get('employee_id')
    current_date = timezone.now().strftime('%Y-%m-%d')
    
    total_services = (SalesByStaffItemService.objects
                    .filter(employee_id=employee_id, date=current_date)
                    .aggregate(total_services=Sum('itemtotal'))['total_services'] or 0) + \
                    (SaleByStaffItem.objects
                    .filter(employee_id=employee_id, date=current_date)
                    .aggregate(total_services=Sum('total_amount'))['total_services'] or 0)

    total_sales = (SalesByStaffItemService.objects
                .filter(employee_id=employee_id, date=current_date)
                .aggregate(total_sales=Sum('servicetotal'))['total_sales'] or 0) + \
                (SaleByStaffService.objects
                .filter(employee_id=employee_id, date=current_date)
                .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0)
    total_collection = total_sales + total_services 

    data = {
        'total_services': total_services,
        'total_sales': total_sales,
        'total_collection': total_collection
    }
    return JsonResponse(data)




class DayClosingRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(DayClosing, pk=pk)

    def get(self, request, pk, format=None):
        day_closing = self.get_object(pk)
        serializer = DayClosingSerializer(day_closing)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        day_closing = self.get_object(pk)
        serializer = DayClosingSerializer(day_closing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        day_closing = self.get_object(pk)
        day_closing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class DayClosingAdminListCreateAPIView(APIView):
    def get(self, request, format=None):
        employee_id = request.session.get('employee_id')
        day_closing_admins = DayClosingAdmin.objects.filter(employee=employee_id)
        serializer = DayClosingAdminSerializer(day_closing_admins, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        employee_id = request.session.get('employee_id')
        employee =get_object_or_404(Employee,id=employee_id)
        serializer = DayClosingAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['employee']=employee
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request, format=None):
        employee_id = request.session.get('employee_id')
        sales_by_staff_service = SaleByStaffService.objects.filter(employee=employee_id)
        serializer = SaleByStaffServiceSerializer(sales_by_staff_service, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        employee_id = request.session.get('employee_id')
        employee =get_object_or_404(Employee,id=employee_id)
        serializer = SaleByStaffServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['employee']=employee
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request, format=None):
        employee_id = request.session.get('employee_id')
        sales_by_staff_item = SaleByStaffItem.objects.filter(employee=employee_id)
        serializer = SalesByStaffItemSerializer(sales_by_staff_item, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        employee_id = request.session.get('employee_id')
        employee =get_object_or_404(Employee,id=employee_id)
        serializer = SalesByStaffItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['employee']=employee
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

    def get(self, request, format=None):
        employee_id = request.session.get('employee_id')
        sales_by_staff_item_service = SalesByStaffItemService.objects.filter(employee=employee_id)
        serializer = SalesByStaffItemServiceSerializer(sales_by_staff_item_service, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        employee_id = request.session.get('employee_id')
        employee = get_object_or_404(Employee,id=employee_id)
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
        del request.session['employee_id']
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)



class EmployeeDashboardAPIView(APIView):
    def get(self, request, format=None):
        # Retrieve the employee ID from the session
        employee_id = request.session.get('employee_id')
        print(employee_id)
        # Fetch employee details
        employee = get_object_or_404(Employee, pk=employee_id)
        
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
        day_closings = DayClosing.objects.filter(employee_id=employee_id, date__gte=first_day_of_month, date__lte=last_day_of_month)
        
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
            'total_services': float(closing.total_services),
            'total_sales': float(closing.total_sales),
            'advance': float(closing.advance),
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
            'business_profile':BussinessProfileSerializer(business_profile).data,
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
    def get(self, request, format=None):
        id =request.session.get('employee_id')
        employee = get_object_or_404(Employee, id=id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class DayClosingReportAPIView(APIView):
    def get(self, request, format=None):
        logged_in_employee_id = request.session.get('employee_id')  # Retrieve the logged-in employee's ID from the session
        # logged_in_employee_id=1
        day_closings_list = DayClosing.objects.filter(employee__id=logged_in_employee_id).order_by('-created_on')
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
        day_closings_json = [{"date": dc.date, "total_services": dc.total_services, "total_sales": dc.total_sales, "total_collection": dc.total_collection} for dc in day_closings]

        return JsonResponse({'day_closings': day_closings_json}, status=status.HTTP_200_OK)


class SalesReportAPIView(APIView):
    def get(self, request, format=None):
        logged_in_employee_id = request.session.get('employee_id')  # Retrieve the logged-in employee's ID from the session
        # logged_in_employee_id=1

        # Query the sales data filtered by the logged-in employee's ID
        sales = SalesByStaffItemService.objects.filter(employee__id=logged_in_employee_id)
        sales_staff_service = SaleByStaffService.objects.filter(employee__id=logged_in_employee_id)
        sales_staff_item = SaleByStaffItem.objects.filter(employee__id=logged_in_employee_id)

        # Convert sales data to JSON
        sales_json = [{"date": s.date, "total_amount": s.total_amount} for s in sales]
        sales_staff_service_json = [{"date": ss.date, "total_amount": ss.total_amount} for ss in sales_staff_service]
        sales_staff_item_json = [{"date": si.date, "total_amount": si.total_amount} for si in sales_staff_item]

        return JsonResponse({'sales': sales_json, 'sales_staff_service': sales_staff_service_json, 'sales_staff_item': sales_staff_item_json}, status=status.HTTP_200_OK)
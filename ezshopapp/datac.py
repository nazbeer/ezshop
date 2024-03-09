from ezshop.ezshopapp.models import SalesByStaffItemService

# Get the queryset for the model
queryset = SalesByStaffItemService.objects.all()

# Delete all records in the model
queryset.delete()

### sales/admin.py ###

# Django
from django.contrib import admin

# Local
from .models import Sale

# Register Sale with customized admin area
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
  list_display  = ('product', 'salesman', 'quantity', 'total', 'created')
  ordering      = ('created',)
  search_fields = ('product',)
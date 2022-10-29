# stocks/admin.py

# django
from django.contrib import admin

# Local
from .models import Stock

# Register your models here.

# Register Stock with customized admin area
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
  list_display  = ('ticker_name', 'ticker_description')
  ordering      = ('ticker_name',)
  search_fields = ('ticker_name', 'ticker_description')

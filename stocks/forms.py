# stocks/forms.py

# django
from django import forms

# local
from .models import Stock

# form to add stock 
class StockForm(forms.ModelForm):
  class Meta:
    model  = Stock
    fields = ('ticker_name',
              'ticker_description')

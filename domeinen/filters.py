# domeinen/filters.py

# packages
import django_filters
from django_filters import DateFilter, CharFilter

# local
from .models import Domein

class DomeinFilter(django_filters.FilterSet):
  #start_date = DateFilter(field_name='start_at', lookup_expr='gte')
  #end_date   = DateFilter(field_name='end_at', lookup_expr='lte')
  url         = CharFilter(field_name='url', lookup_expr='icontains')
  description = CharFilter(field_name='description', lookup_expr='icontains')
  
  class Meta:
    model     = Domein
    # fields  = '__all__'
    # exclude = ['uuid', 'start_at', 'end_at']
    fields    = ['url', 'website', 'description']
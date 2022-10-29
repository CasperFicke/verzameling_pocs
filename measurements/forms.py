# measurements/forms.py

from django import forms

# Local
from .models import Measurement, Endpoint

# Measurementform
class MeasurementForm(forms.ModelForm):
  class Meta:
    model  = Measurement
    fields = ('location', 'destination',)

# Endpointform
class EndpointForm(forms.ModelForm):
  class Meta:
    model  = Endpoint
    fields = ('location', 'bearing', 'dist_km', 'dist_nm',)

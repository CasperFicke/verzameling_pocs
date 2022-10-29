### csvs/forms.py ###

# Django
from django import forms

# Local
from .models import Csv

class CsvModelForm(forms.ModelForm):
  class Meta:
    model  = Csv
    fields = ('file_name',)
### csvs/admin.py ###

# Django
from django.contrib import admin

# Local
from .models import Csv

# Register your models here.

# Register Csv
admin.site.register(Csv)
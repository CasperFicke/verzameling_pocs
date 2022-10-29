# measurements/admin.py

# django
from django.contrib import admin

# local
from .models import Measurement, Endpoint

# Register Models
myModels = [Measurement, Endpoint]  # iterable list
# overall adminarea
admin.site.register(myModels)
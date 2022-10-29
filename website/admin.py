### ADMIN.PY WBSITE APP ###

# Django
from django.contrib import admin

# Local
from .models import Course

# Register your models here.
myModels = [Course]  # iterable list
admin.site.register(myModels)

# users/admin.py

# Django
from django.contrib import admin
from django.contrib.auth.models import Group

# Local
from .models import UserProfile

# Register your models here.
myModels = [UserProfile]  # iterable list
admin.site.register(myModels)

# Unregister models
# admin.site.unregister(Group)

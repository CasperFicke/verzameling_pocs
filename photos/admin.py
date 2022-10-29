# fotos/admin.py

# django
from django.contrib import admin

# local
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
  list_display = ('name', 'description', 'image_tag',)
  ordering     = ('name',)
  list_filter  = ('name', 'description',)

admin.site.register(Photo, PhotoAdmin)
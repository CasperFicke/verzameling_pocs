# energie/admin.py

# Django
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Local
from .models import (
  Energietype,
  Medium,
  Meter,
  Meterstand
  )

# Register Energietype with customized admin area
@admin.register(Energietype)
class EnergietypeAdmin(admin.ModelAdmin):
  list_display  = ('name', 'description')
  ordering      = ('name',)
  
# Register Medium with customized admin area
@admin.register(Medium)
class MediumAdmin(admin.ModelAdmin):
  list_display  = ('name', 'description')
  ordering      = ('name',)
  search_fields = ('name',)

# Register Meter with customized admin area
@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
  list_display  = ('name', 'medium', 'description', 'metertype')
  ordering      = ('name', 'medium')
  search_fields = ('name',)

# Register Meterstand with customized admin area
#@admin.register(Meterstand)
class MeterstandAdmin(ImportExportModelAdmin):
  fields        = ('meter', 'meterstand_date', 'meterstand_waarde', 'opnemer')
  list_display  = ('meter', 'meterstand_date', 'meterstand_waarde', 'opnemer')
  list_filter   = ('meter', 'opnemer')
  ordering      = ('meter', 'meterstand_date',)
  search_fields = ('meter', 'opnemer',)

admin.site.register(Meterstand, MeterstandAdmin)
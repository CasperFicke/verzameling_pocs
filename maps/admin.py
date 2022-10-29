# maps/admin.py

# django
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Local
from .models import Metadata, Hook, Actie, Land, Plaats, Unemploymentrate

# Register your models here.
# Dataimportexportadmin

# Register Metadata
class MetadataAdmin(admin.ModelAdmin):
  list_display  = ('naam', 'beschrijving', 'referentie', 'beheerder', 'updated')
  ordering      = ('naam',)

# Register Land
class LandAdmin(ImportExportModelAdmin):
  list_display  = ('naam', 'latitude', 'longitude', 'aant_inwoners')
  ordering      = ('naam',)

# Register Plaats
class PlaatsAdmin(ImportExportModelAdmin):
  list_display  = ('naam', 'latitude', 'longitude', 'aant_inwoners')
  ordering      = ('naam',)

# Register Unemploymentrate
class UnemploymentrateAdmin(ImportExportModelAdmin):
  list_display  = ('state', 'percentage')
  ordering      = ('state',)

# overall admin area 
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(Plaats, PlaatsAdmin)
admin.site.register(Unemploymentrate, UnemploymentrateAdmin)

# Register Models
myModels = [Hook, Actie]  # iterable list
# overall adminarea
admin.site.register(myModels)
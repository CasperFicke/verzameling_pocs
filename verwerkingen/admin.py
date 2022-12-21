# verwerkingen/admin.py

# django
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# local
from .models import (
  Gemeente,
  Verordening,
  Ontvanger,
  Verantwoordelijke,
  Team,
  Grondslag,
  Persoonsgegeven,
  Verwerker,
  Verwerkersovereenkomst,
  Betrokkene,
  Ontvanger,
  Hoofdproces,
  Verwerking
  )

# Register Verordening
class VerordeningAdmin(ImportExportModelAdmin):
  list_display = ('naam', 'beschrijving',)
  ordering     = ('naam',)
# overall admin area
admin.site.register(Verordening, VerordeningAdmin)

# Register Verantwoordelijke
class VerantwoordelijkeAdmin(ImportExportModelAdmin):
  list_display = ('naam',)
  ordering     = ('naam',)
# overall admin area
admin.site.register(Verantwoordelijke, VerantwoordelijkeAdmin)

# Register Grondslag
class GrondslagAdmin(ImportExportModelAdmin):
  list_display = ('naam',)
  ordering     = ('naam',)
# overall admin area
admin.site.register(Grondslag, GrondslagAdmin)

# Register Persoonsgegeven
class PersoonsgegevenAdmin(ImportExportModelAdmin):
  list_display = ('type', 'beschrijving',)
  ordering     = ('type',)
# overall admin area
admin.site.register(Persoonsgegeven, PersoonsgegevenAdmin)

# Register Verwerkersovereenkomst
class VerwerkersovereenkomstAdmin(admin.ModelAdmin):
  list_display = ('naam', 'verwerker', 'pdf', 'extern',)
  ordering     = ('naam',)
# overall admin area
admin.site.register(Verwerkersovereenkomst, VerwerkersovereenkomstAdmin)

# Register Verwerking
class VerwerkingAdmin(ImportExportModelAdmin):
  list_display = ('naam', 'doel', 'buitenEUgedeeld', 'dpia_uitgevoerd',)
  ordering     = ('naam',)
# overall admin area
admin.site.register(Verwerking, VerwerkingAdmin)

# Register Betrokkene
class BetrokkeneAdmin(ImportExportModelAdmin):
  list_display = ('naam', 'beschrijving',)
  ordering     = ('naam',)
# overall admin area
admin.site.register(Betrokkene, BetrokkeneAdmin)

# Register Models without layout:
myModels = [Gemeente, Team, Verwerker, Ontvanger, Hoofdproces]
# overall adminarea
admin.site.register(myModels)
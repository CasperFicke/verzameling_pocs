# verwerkingen/admin.py

# django
from django.contrib import admin

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
class VerordeningAdmin(admin.ModelAdmin):
  list_display = ('naam', 'beschrijving',)
  ordering     = ('naam',)

# overall admin area
admin.site.register(Verordening, VerordeningAdmin)

# Register Verwerkersovereenkomst
class VerwerkersovereenkomstAdmin(admin.ModelAdmin):
  list_display = ('naam', 'verwerker', 'pdf', 'extern',)
  ordering     = ('naam',)

# overall admin area
admin.site.register(Verwerkersovereenkomst, VerwerkersovereenkomstAdmin)

# Register Verwerking
class VerwerkingAdmin(admin.ModelAdmin):
  list_display = ('naam', 'doel', 'buitenEUgedeeld', 'dpia_uitgevoerd',)
  ordering     = ('naam',)

# overall admin area
admin.site.register(Verwerking, VerwerkingAdmin)

# Register Models without layout:
myModels = [Gemeente, Verantwoordelijke, Team, Grondslag, Persoonsgegeven, Verwerker,Betrokkene, Ontvanger, Hoofdproces]
# overall adminarea
admin.site.register(myModels)
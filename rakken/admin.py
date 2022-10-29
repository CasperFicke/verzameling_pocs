# rakken/admin.py

# Django
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Local
from .models import (
  Weer,
  Evenement,
  WaypointType,
  Waypoint,
  RakType,
  Rak,
  RakScore,
  Baan,
  Boot,
  PolarpuntType,
  Polarpunt
  )

# Register Weertype
class WeerAdmin(admin.ModelAdmin):
  list_display = ('windkracht', 'windrichting')
 
# overall admin area
admin.site.register(Weer, WeerAdmin)

# Register Evenementtype
class EvenementAdmin(admin.ModelAdmin):
  list_display = ('naam', 'beschrijving', 'datum')
  ordering     = ('datum', 'naam',)

# overall admin area
admin.site.register(Evenement, EvenementAdmin)

# Register Waypointtype
class WaypointTypeAdmin(admin.ModelAdmin):
  list_display = ('type', 'beschrijving',)
  ordering     = ('type',)

# overall admin area
admin.site.register(WaypointType, WaypointTypeAdmin)

# Register Waypoint
class WaypointAdmin(ImportExportModelAdmin):
  list_display = ('naam', 'type', 'omschrijving', 'latitude', 'longitude',)
  ordering     = ('naam',)

# overall admin area
admin.site.register(Waypoint, WaypointAdmin)


# Register Raktype
class RakTypeAdmin(admin.ModelAdmin):
  list_display = ('type', 'beschrijving', 'max_aantal',)
  ordering     = ('type',)

# overall admin area
admin.site.register(RakType, RakTypeAdmin)


# Register Rak
class RakAdmin(ImportExportModelAdmin):
  list_display = ('uuid', 'evenement', 'waypoint1', 'waypoint2', 'lengte', 'afstand', 'type',)
  ordering     = ('evenement', 'waypoint1',)
  list_filter  = ('evenement', 'type', 'waypoint1')

# overall admin area
admin.site.register(Rak, RakAdmin)


# Register RakScore
class RakScoreAdmin(admin.ModelAdmin):
  list_display = ('uuid', 'twa', 'score', )
  ordering     = ('uuid',)
 
# overall admin area
admin.site.register(RakScore, RakScoreAdmin)


# Register baan
class BaanAdmin(admin.ModelAdmin):
  list_display = ('naam', 'beschrijving',)
  ordering     = ('naam',)

# overall admin area
admin.site.register(Baan, BaanAdmin)


# Register Boot
class BootAdmin(ImportExportModelAdmin):
  list_display = ('naam', 'model', 'gph', 'toelichting',)
  ordering     = ('naam',)

# overall admin area
admin.site.register(Boot, BootAdmin)

# Register Polarpunttype
class PolarpuntTypeAdmin(admin.ModelAdmin):
  list_display = ('type', 'beschrijving',)
  ordering     = ('type',)

# overall admin area
admin.site.register(PolarpuntType, PolarpuntTypeAdmin)

# Register Polarpunt
class PolarpuntAdmin(admin.ModelAdmin):
  list_display = ('boot', 'windspeed', 'twa', 'boatspeed', 'type')
  ordering     = ('boot', 'windspeed', 'twa',)

# overall admin area
admin.site.register(Polarpunt, PolarpuntAdmin)


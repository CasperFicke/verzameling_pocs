# meetups/admin.py

from django.contrib import admin

# Local
from .models import Deelnemer, Meetup, Location

# Register Meetup
class MeetupAdmin(admin.ModelAdmin):
  list_display        = ('title', 'date', 'location')
  list_filter         = ('location','date')
  ordering            = ('title',)
  prepopulated_fields = {'slug': ('title',)}

# overall admin area 
admin.site.register(Meetup, MeetupAdmin)
admin.site.register(Location)
admin.site.register(Deelnemer)
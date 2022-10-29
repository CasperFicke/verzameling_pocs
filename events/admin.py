# events/admin.py

# Django
from django.contrib import admin

# Local
from .models import Event, Venue, Visitor

# Events admin area
class EventsAdminArea(admin.AdminSite):
  site_header = 'Events Admin Area'
  index_title = "Events Admin"
  site_title  = "Oefenapplicatie"

events_adminsite = EventsAdminArea(name = 'EventsAdmin')

# Models

# Register Visitor
admin.site.register(Visitor)

# Register Venue with customized admin area
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
  list_display  = ('name', 'adres', 'telefoon', 'image_tag', 'owner',)
  ordering      = ('name',)
  search_fields = ('name', 'adres')
  fields        = ('name', ('adres', 'postcode', 'plaats'), ('telefoon', 'email'), ('website', 'image'))

# Register Event with customized admin area
#@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
 
  list_display  = ('name', 'event_start', 'event_end', 'venue', 'approved')
  ordering      = ('event_start',)
  list_filter   = ('event_start', 'venue')
  search_fields = ('name', 'venue')
  fields        = (('name', 'venue'), ('event_start', 'event_end'), 'description', 'manager', 'approved', 'attendees')

admin.site.register(Event, EventAdmin)

# Register models for dedicated admin area
myModels = [Event, Venue, Visitor]  # iterable list
events_adminsite.register(myModels)
# events/urls.py

# Django
from django.urls import path

# local
from . import views

urlpatterns = [
  # VENUES
  path('venues/'                    , views.all_venues, name="all_venues"), # static view
  path('venues/csv/'                , views.csv_venues, name="csv_venues"),
  path('venues/txt/'                , views.txt_venues, name="txt_venues"),
  path('venues/pdf/'                , views.pdf_venues, name="pdf_venues"),
  path('venues/search/'             , views.search_venues, name="search_venues"),
  path('venues/add/'                , views.add_venue, name="add_venue"),
  path('venues/favoriet/'           , views.AddFavorietView.as_view(), name="add-favoriet-venue"),
  path('venues/<venue_uuid>/'       , views.show_venue, name="show_venue"), # dynamic view
  #path('venues/<venue_uuid>/'      , views.show_venueView.as_view(), name="show_venue"), # class based (eerst uuid als pk zetten)
  path('venues/<venue_uuid>/edit/'  , views.edit_venue, name="edit_venue"),
  path('venues/<venue_uuid>/delete/', views.delete_venue, name="delete_venue"),
  path('venues/<venue_uuid>/pdf/'   , views.pdf_venue, name="pdf_venue"),
  path('venues/<venue_uuid>/qrcode/', views.qrcode_venue, name="qrcode-venue"),

  # AGENDA
  path('events/agenda/'                             , views.agenda, name="agenda"),
  path('events/agenda/<int:year>/<int:monthnumber>/', views.agenda_by_monthnumber , name="agenda_bymonthnumber"), # path converters
  path('events/agenda/<int:year>/<str:month>/'      , views.agenda , name="agenda"), # path converters
  path('events/kalender/'                           , views.CalendarView.as_view(), name='kalender'),

  # EVENTS
  path('events/'                , views.all_events, name="all_events"),
  path('events/my_events/'      , views.my_events, name='my_events'),
  path('events/event_approval/' , views.event_approval, name='event-approval'),
  path('events/add/'            , views.add_event, name='add_event'),
  path('events/<event_id>/<slug:event_slug>/'       , views.show_event, name='show_event'),
	path('events/<event_id>/<slug:event_slug>/edit/'  , views.edit_event, name='edit_event'),
  path('events/<event_id>/<slug:event_slug>/delete/', views.delete_event, name="delete_event"),
]

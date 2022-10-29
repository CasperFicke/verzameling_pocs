# events/forms.py

# Django
from django import forms
from django.forms import ModelForm, DateInput

# Local
from .models import Venue, Event

# Venue form
class VenueForm(ModelForm):
  class Meta:
    model  = Venue
    fields = ('name', 'adres', 'postcode', 'plaats', 'telefoon', 'website', 'email', 'image')
    labels  = {
      'name'    : 'Venue naam',
      'adres'   : 'adres',
      'postcode': 'postcode',
      'plaats'  : 'plaats',
      'telefoon': 'telefoon',
      'website' : 'website',
      'email'   : 'e-mail',
      'image'   : 'image',
    }
    widgets = {
      'name'     : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'naam'}),
      'adres'    : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'straatnaam huisnummer'}),
      'postcode' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 AB'}),
      'plaats'   : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'plaatsnaam'}),
      'telefoon' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0123456789'}),
      'website'  : forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://xxx.yyy'}),
      'email'    : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'aaa@bbb.ccc'})
    }

# Admin SuperUser Event form
class EventFormAdmin(ModelForm):
  class Meta:
    model = Event
    # fields = '__all__'
    fields = ('name', 'description', 'event_start', 'event_end', 'venue', 'manager', 'approved', 'attendees')
    labels  = {
      'name'       : 'Event naam',
      'description': 'Omschrijving',
      'event_start': 'Aanvang',
      'event_end'  : 'Einde',
      'venue'      : 'Locatie',
      'manager'    : 'Event-manager',
      'attendees'  : 'Bezoekers'
    }
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'name'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eventnaam'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'eventbeschrijving...', 'rows': 4}),
      'event_start': DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'event_end'  : DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'venue'      : forms.Select(attrs={'class': 'form-select', 'placeholder': 'venue'}),
      'manager'    : forms.Select(attrs={'class': 'form-select', 'placeholder': 'plaatsnaam'}),
      'attendees'  : forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'plaatsnaam'}),
    }

  def __init__(self, *args, **kwargs):
    super(EventFormAdmin, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['event_start'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['event_end'].input_formats = ('%Y-%m-%dT%H:%M',)

# User Event form
class EventForm(ModelForm):
  class Meta:
    model = Event
    # fields = '__all__'
    fields = ('name', 'description', 'event_start', 'event_end', 'venue', 'attendees')
    labels  = {
      'name'       : 'Event naam',
      'description': 'Omschrijving',
      'event_start': 'Aanvang',
      'event_end'  : 'Einde',
      'venue'      : 'Locatie',
      'attendees'  : 'Bezoekers'
    }
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'name'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eventnaam'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'eventbeschrijving...', 'rows': 4}),
      'event_start': DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'event_end'  : DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'venue'      : forms.Select(attrs={'class': 'form-select', 'placeholder': 'venue'}),
      'attendees'  : forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'deelnemers'}),
    }

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['event_start'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['event_end'].input_formats = ('%Y-%m-%dT%H:%M',)
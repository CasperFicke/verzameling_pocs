# domeinen/forms.py

# Django
from django import forms
from django.forms import ModelForm, DateInput

# Local
from .models import Domein, Contact

# Domeinform
class DomeinForm(ModelForm):
  class Meta:
    model = Domein
    # fields = '__all__'
    fields = ('url', 'description', 'start', 'end', 'betrokkenen')
    # exclude = ('slug', 'uuid', 'start_at', 'end_at', 'created')
    labels  = {
      'url'         : 'URL van het domein',
      'description' : 'Omschrijving',
      'start'       : 'Start geldigheid',
      'end'         : 'Einde geldigheid',
      'betrokkenen' : 'Betrokkene(n)'
    }
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'url'         : forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL van het domein'}),
      'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'hier uw domeinbeschrijving...', 'rows': 4}),
      'start'       : DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
      'end'         : DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
      'betrokkenen' : forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'betrokkenen'}),
    }

  # waar was dit ook alweer voor??
  def __init__(self, *args, **kwargs):
    super(DomeinForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start'].input_formats = ('%Y-%m-%d',)
    self.fields['end'].input_formats = ('%Y-%m-%d',)

# Contactform
class ContactForm(ModelForm):
  class Meta:
    model = Contact
    fields = ('organisatie', 'name', 'rol', 'adres', 'postcode', 'plaats', 'telefoon', 'email')
    labels  = {
      'organisatie' : 'Organisatie',
      'name'        : 'Naam contactpersoon',
      'rol'         : 'Rol van dit contact',
      'adres'       : 'Straatnaam & huisnummer',
      'postcode'    : 'Postcode',
      'plaats'      : 'Plaats',
      'telefoon'    : 'Telefoon',
      'email'       : 'E-mail'
    }
    widgets = {
      'organisatie' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'naam van de organisatie'}),
      'name'        : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'naam van de contactpersoon'}),
      'rol'         : forms.Select(attrs={'class': 'form-select', 'placeholder': 'rol'}),
      'adres'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'straatnaam en huisnummer'}),
      'postcode'    : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'postcode'}),
      'plaats'      : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'plaats'}),
      'telefoon'    : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'telefoon'}),
      'email'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e-mail'}),
    }

  # beschrijving van deze functie
  def __init__(self, *args, **kwargs):
    super(ContactForm, self).__init__(*args, **kwargs)

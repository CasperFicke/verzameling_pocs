# users/models.py

# Django
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# installed packages
import pycountry

# python
from operator import itemgetter

#these are model abstracts from django extensions
from django_extensions.db.models import (
  TimeStampedModel,
	ActivatorModel 
)

# create sortedlist of country codes
country_list = sorted(
  [(country.name, country.name) 
  for country in list(pycountry.countries)],
    key=itemgetter(0)
)
country_list.insert(0, ("*Select Country", "*Select Country"))
#(('United Kingdom', 'United Kingdom'), ('France', 'France').....)
COUNTRIES = country_list

# Userprofile model
class UserProfile(models.Model):
  bio          = models.TextField(null=True, blank=True)
  profile_pic  = models.ImageField(default='images/profile/standard.jpg', null=True, blank=True, upload_to="images/profile/")
  country      = models.CharField(verbose_name="Country",max_length=100, null=True, blank=True, choices=COUNTRIES)
  website_url  = models.CharField(max_length=255, null=True, blank=True)
  twitter_url  = models.CharField(max_length=255, null=True, blank=True)
  facebook_url = models.CharField(max_length=255, null=True, blank=True)
  # relaties
  user         = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  # secundair
  is_active    = models.BooleanField(default=True)
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the Userprofile was created or updated')
  updated      = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name_plural = 'User profiles'
    ordering = ["id"]

  # functie om userprofile in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.user}'

  # functie om redirect url te bepalen
  def get_absolute_url(self):
    return reverse('index')

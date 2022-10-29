# meetups/models.py

from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField, EmailField

# Location model
class Location(models.Model):
  naam   = models.CharField(max_length=150)
  adres  = models.CharField(max_length=200)

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.naam} - {self.adres}'

class Deelnemer(models.Model):
  email = models.EmailField(unique=True)
  
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.email

class Meetup(models.Model):
  title       = models.CharField(max_length=100)
  slug        = models.SlugField(unique=True)
  description = models.TextField(max_length=250)
  image       = models.ImageField(upload_to= 'images/meetups/', blank=True)
  organiser   = models.EmailField(blank=True, null=True)
  date        = models.DateField(blank=True)
  # relaties
  location    = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL, related_name='meetups')
  deelnemers  = models.ManyToManyField(Deelnemer, blank=True, related_name='meetups')
  
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.title} - {self.location}'

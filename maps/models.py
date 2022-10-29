# maps/models.py

from django.db import models
from django.db.models.base import Model
from django.contrib.contenttypes.models import ContentType

import geocoder

# metadata model
class Metadata(models.Model):
  naam         = models.CharField(max_length=100, unique=True)
  beschrijving = models.TextField(max_length=400,null=True, blank=True)
  referentie   = models.URLField(max_length=100, null=True, blank=True)
  beheerder    = models.CharField(max_length=100, null=True, blank=True)
  created      = models.DateTimeField(auto_now_add=True)
  updated      = models.DateTimeField(auto_now=True)
  # relaties
  model        = models.OneToOneField(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
 
  class Meta:
    verbose_name_plural = 'metadata'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# actie model
class Actie(models.Model):
  naam      = models.CharField(max_length=100, unique=True)
  # secundary
  created      = models.DateTimeField(auto_now_add=True)
  updated      = models.DateTimeField(auto_now=True)
 
  class Meta:
    verbose_name_plural = 'acties'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.naam}'

# hook model
class Hook(models.Model):
  gegeven      = models.CharField(max_length=100, unique=True)
  # relaties
  actie        = models.ManyToManyField(Actie, blank=True)
  endpoint     = models.URLField(max_length=100, null=True, blank=True)
  # secundary
  created      = models.DateTimeField(auto_now_add=True)
  updated      = models.DateTimeField(auto_now=True)
 
  class Meta:
    verbose_name_plural = 'hooks'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.gegeven} - {self.endpoint}'

# Land model
class Land(models.Model):
  naam          = models.CharField(max_length=100, unique=True)
  latitude      = models.FloatField(default=0)
  longitude     = models.FloatField(default=0)
  aant_inwoners = models.PositiveIntegerField(null=True)
 
  class Meta:
    verbose_name_plural = 'landen'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Plaatsmodel
class Plaats(models.Model):
  naam          = models.CharField(max_length=100, unique=True)
  aant_inwoners = models.PositiveIntegerField(null=True)
  latitude      = models.FloatField(default=0)
  longitude     = models.FloatField(default=0)
 
  class Meta:
    verbose_name_plural = 'plaatsen'

  # functie die lat en long ophaalt mbv geocoder en in object bewaard
  def save(self, *args, **kwargs):
    self.latitude  = geocoder.osm(self.naam).lat
    self.longitude = geocoder.osm(self.naam).lng
    return super().save(*args, **kwargs)

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Unemploymentrate model
class Unemploymentrate(models.Model):
  state      = models.CharField(max_length=30)
  percentage = models.DecimalField(max_digits=5, decimal_places=2)
  
  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.state
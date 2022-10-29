# measurements/models.py

import uuid

from django.db import models
from django.db.models.base import Model

# Afstand meten
class Measurement(models.Model):
  location    = models.CharField(max_length=200)
  destination = models.CharField(max_length=200)
  dist_km     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  dist_nm     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  bearing     = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
  # secundair
  uuid        = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  created     = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.location} - {self.destination}; Afstand is {self.dist_km} km, richting is {self.bearing}°'

# Endpoint bepalen meten
class Endpoint(models.Model):
  location    = models.CharField(max_length=200)
  bearing     = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
  dist_km     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  dist_nm     = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  # secundair
  uuid        = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  created     = models.DateTimeField(auto_now_add=True)
  
  # functie die afstand in zeemijlen berekend
  def save(self, *args, **kwargs):
    self.dist_nm  = self.dist_km*1000/1852
    return super().save(*args, **kwargs)

  def __str__(self):
    return f'{self.location} - {self.bearing}°; Afstand is {self.dist_km} km / {self.dist_nm} nm'
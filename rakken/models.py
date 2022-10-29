# rakken/models.py

# django
from django.urls import reverse
from django.db import models

# installed packages
import uuid
from geopy.distance  import geodesic
from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84

# abstracts from django extensions
from django_extensions.db.models import (
  TimeStampedModel,
	ActivatorModel 
)

# Weermodel
class Weer(models.Model):
  windkracht   = models.PositiveIntegerField('windkracht (knt)', default=0)
  windrichting = models.FloatField('windrichting', default=0)
 
  class Meta:
    verbose_name_plural = 'weer'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'windkracht: {self.windkracht} - windrichting: {self.windrichting}'


# Evenement model
class Evenement(TimeStampedModel, ActivatorModel, models.Model):
  naam         = models.CharField('Evenement naam', max_length=100)
  beschrijving = models.TextField('Beschrijving', blank=True)
  datum        = models.DateField('Datum', blank=True, null=True, help_text='Datum van het evenement')
  # secundair
  uuid         = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the event record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the evenement record')
  
  class Meta:
    verbose_name_plural = 'Evenementen'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# WaypointType model
class WaypointType(models.Model):
  type         = models.CharField('Waypoint Type', max_length=100)
  beschrijving = models.TextField('Beschrijving', blank=True)
  # secundair
  uuid         = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the waypointtype record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the waypointtype record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the waypointtype was registered in the system')

  class Meta:
    verbose_name_plural = 'waypoint types'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.type

# Waypointmodel
class Waypoint(models.Model):
  naam         = models.CharField('Waypoint naam', max_length=255, help_text='Naam van het waypoint', unique=True)
  omschrijving = models.TextField('Waypoint Omschrijving', blank=True, help_text='Omschrijving van het waypoint')
  latitude     = models.FloatField(default=0)
  longitude    = models.FloatField(default=0)
  # relaties
  type         = models.ForeignKey(WaypointType, blank=True, null=True, on_delete=models.SET_NULL, related_name='waypoints')
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the waypoint record')
  end_at       = models.DateField('end at', blank=True, null=True, help_text='End date of the waypoint record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the waypoint was registered in the system')
 
  class Meta:
    verbose_name_plural = 'waypoints'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Raktype model
class RakType(models.Model):
  type         = models.CharField('Rak Type', max_length=100)
  beschrijving = models.TextField('Beschrijving', blank=True)
  max_aantal   = models.PositiveIntegerField('Maximaal aantal keren te varen', null=True)
  # secundair
  uuid         = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the record was registered in the system')

  class Meta:
    verbose_name_plural = 'rak types'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.type

# Rakmodel
class Rak(models.Model):
  lengte    = models.FloatField('Raklengte volgens organisatie', blank=True, null=True)
  # relaties
  evenement = models.ForeignKey(Evenement, blank=True, null=True, on_delete=models.CASCADE, related_name='rakken')
  waypoint1 = models.ForeignKey(Waypoint, blank=True, null=True, on_delete=models.CASCADE, related_name='waypoint1')
  waypoint2 = models.ForeignKey(Waypoint, blank=True, null=True, on_delete=models.CASCADE, related_name='waypoint2')
  type      = models.ForeignKey(RakType, blank=True, null=True, on_delete=models.SET_NULL, related_name='rakken')
  # secundair
  uuid      = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at  = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at    = models.DateField('end at', blank=True, null=True, help_text='End date of the record')
  created   = models.DateTimeField(auto_now_add=True, help_text='Date when the record was registered in the system')
 
  class Meta:
    verbose_name_plural = 'rakken'

  # method to calculate afstand tussen waypoints vh rak
  @property
  def afstand(self):
    wp1 = (self.waypoint1.latitude, self.waypoint1.longitude)
    wp2 = (self.waypoint2.latitude, self.waypoint2.longitude)
    raklengte = round(geodesic(wp1, wp2).nm, 4)
    return raklengte

  # method to calculate bearing
  @property
  def bearing12(self):
    g = geod.Inverse(self.waypoint1.latitude, self.waypoint1.longitude, self.waypoint2.latitude, self.waypoint2.longitude)
    ri =  g['azi1']
    if ri < 0:
      ri += 360
    return round(ri, 1)
  
  @property
  def bearing21(self):
    if self.bearing12 > 180:
      return round(self.bearing12 - 180, 1)
    else:
      return round(self.bearing12 + 180, 1)
  
  # functie om model in de admin web-pagina te kunnen presenteren
  #def __str__(self):
  #  return self.uuid

# Rakscore-model
class RakScore(models.Model):
  waypoint1 = models.ForeignKey(Waypoint, blank=True, null=True, on_delete=models.CASCADE, related_name='rakscoreswp1')
  waypoint2 = models.ForeignKey(Waypoint, blank=True, null=True, on_delete=models.CASCADE, related_name='rakscoreswp2')
  bearing   = models.FloatField('bearing', blank=True, null=True)
  twa       = models.FloatField('twa', blank=True, null=True)
  score     = models.TextField('score', blank=True, null=True)
  color     = models.TextField('kleurscore', blank=True, null=True)
  #twa21   = models.FloatField('twa van waypoint2 naar waypoint1', blank=True, null=True)
  #score21 = models.TextField('score van waypoint2 naar waypoint1', blank=True, null=True)
  #color21 = models.TextField('kleurscore van waypoint2 naar waypoint1', blank=True, null=True)
  # relaties
  weer    = models.ForeignKey(Weer, blank=True, null=True, on_delete=models.CASCADE, related_name='rakscores')
  rak     = models.ForeignKey(Rak, blank=True, null=True, on_delete=models.CASCADE, related_name='rakscores')
  # secundair
  uuid    = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  created = models.DateTimeField(auto_now_add=True, help_text='Date when the record was first registered in the system')
 
  class Meta:
    verbose_name_plural = 'rakscores'

  # functie om model in de admin web-pagina te kunnen presenteren
  #def __str__(self):
  #  return self.uuid

# Baan model
class Baan(models.Model):
  naam         = models.CharField('Naam van de baan', max_length=100)
  beschrijving = models.TextField('Beschrijving', blank=True)
  #windkracht   = models.FloatField('windkracht (knt)', default=0)
  #windrichting = models.PositiveIntegerField('windrichting', default=0)
  # relaties
  evenement    = models.ForeignKey(Evenement, blank=True, null=True, on_delete=models.CASCADE, related_name='banen')
  weer         = models.ForeignKey(Weer, blank=True, null=True, on_delete=models.CASCADE, related_name='banen')
  rak          = models.ManyToManyField(Rak, blank=True, related_name='banen')
  # secundair
  uuid         = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the baan record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the baan record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the baan was registered in the system')

  class Meta:
    verbose_name_plural = 'banen'

 # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.naam} - windkracht: {self.weer.windkracht} - windrichting: {self.weer.windrichting}'
  
# Boot model
class Boot(models.Model):
  naam         = models.CharField('Naam', max_length=255, help_text='Naam van de boot')
  model        = models.CharField('Model', blank=True, max_length=255, help_text='Model boot')
  toelichting  = models.TextField('Toelichting', blank=True, help_text='Toelichting bij deze boot')
  gph          = models.FloatField('GPH', blank=True, null=True, help_text='GPH van deze boot')
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the boot record')
  end_at       = models.DateField('end at', blank=True, null=True, help_text='End date of the boot record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the boot was registered in the system')
 
  class Meta:
    ordering = ['naam']
    verbose_name_plural = 'boten'
  
  def get_absolute_url(self):
    return reverse("rakken:show-boot", args=[self.uuid])

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Polarpuntype model
class PolarpuntType(models.Model):
  type         = models.CharField('Polarpunt Type', max_length=100)
  beschrijving = models.TextField('Beschrijving', blank=True)
  # secundair
  uuid         = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the record was registered in the system')

  class Meta:
    verbose_name_plural = 'polarpunt types'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.type

# Polarpunt model
class Polarpunt(models.Model):
  windspeed  = models.PositiveIntegerField('windspeed')
  twa        = models.FloatField('ware windhoek', default=0)
  boatspeed  = models.FloatField('predicted boatspeed', blank=True, null=True)
  vmg        = models.FloatField('predicted VMG', blank=True, null=True)
  # relaties
  type       = models.ForeignKey(PolarpuntType, blank=True, null=True, on_delete=models.SET_NULL, related_name='polarpunten')
  boot       = models.ForeignKey(Boot, null=True, on_delete=models.CASCADE, related_name='polarpunten')
  # secundair
  uuid       = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at   = models.DateField('start at', auto_now=True, help_text='Start date of therecord')
  end_at     = models.DateField('end at', blank=True, null=True, help_text='End date of the record')
  created    = models.DateTimeField(auto_now_add=True, help_text='Date when the record was registered in the system')
 
  class Meta:
    verbose_name_plural = 'polarpunten'

  # functie om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.boot.naam} - tws: {self.windspeed} - twa: {self.twa} - boatspeed: {self.boatspeed}'

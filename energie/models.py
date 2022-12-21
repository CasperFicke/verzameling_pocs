# energie/models.py

# Django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Energietype model
class Energietype(models.Model):
  # attributes
  name        = models.CharField('Energietype Name', max_length=100, unique=True)
  description = models.CharField(max_length=255, blank=True)
  
  # method om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.name

# Medium model
class Medium(models.Model):
  # attributes
  name         = models.CharField('Medium Name', max_length=100, unique=True)
  description  = models.CharField(max_length=255, blank=True)
  energietype  = models.ForeignKey(Energietype, blank=True, null=True, on_delete=models.SET_NULL, related_name='mediums')
  
  # method om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.name

# Meter model
class Meter(models.Model):
  # attributes
  name        = models.CharField('Meter Name', max_length=100, unique=True)
  eenheid     = models.CharField('Meter Eenheid', max_length=10)
  description = models.CharField(max_length=255, blank=True)
  metertype   = models.CharField('Meter type', max_length=100, blank=True)
  # relaties
  medium      = models.ForeignKey(Medium, blank=True, null=True, on_delete=models.SET_NULL, related_name='meters')

  # methode om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.name

# Meterstand model
class Meterstand(models.Model):
  class Meta:
    verbose_name_plural = 'meterstanden'
  # attributes
  meterstand_waarde = models.FloatField('Meterstand Waarde', validators = [MinValueValidator(0), MaxValueValidator(100000)])
  meterstand_date   = models.DateTimeField('Meterstand Date')
  # relaties
  meter             = models.ForeignKey(Meter, blank=True, null=True, on_delete=models.CASCADE)
  opnemer           = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

   # method om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return str(self.meter)

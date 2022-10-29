# domeinen/models.py

import uuid

# Django
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.query_utils import subclasses
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from datetime import date

# Server model
class Server(models.Model):
  naam        = models.CharField('Servernaam', max_length=100)
  description = models.TextField('Beschrijving', blank=True)
  # secundair
  uuid        = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  
  class Meta:
    ordering = ['naam']
  
  def get_absolute_url(self):
    return reverse("show-server", args=[self.uuid])
  
  # functie om server in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.naam

# Service model
class Service(models.Model):
  naam        = models.CharField('Servicenaam', max_length=100)
  description = models.TextField('Beschrijving', blank=True)
  # relaties
  server      = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='services')
  # secundair
  uuid        = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  
  class Meta:
    ordering = ['naam', 'server']
  
  def get_absolute_url(self):
    return reverse("show-service", args=[self.uuid])
  
  # functie om service in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.naam} - staat op server: {self.server.naam}'

# Rol model
class Rol(models.Model):
  rol         = models.CharField('Contact Rol', max_length=100)
  description = models.TextField('Beschrijving', blank=True)
  # secundair
  uuid        = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at    = models.DateField('start at', auto_now=True, help_text='Start date of the rol record')
  end_at      = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the rol record')
  created     = models.DateTimeField(auto_now_add=True, help_text='Date when the rol was registered in the system')

  class Meta:
    verbose_name_plural = 'rollen'

  # create absolute url to show rol
  def get_absolute_url(self):
    return reverse("show-contact", args=[self.uuid])

  # functie om rol in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.rol

# Contact model
class Contact(models.Model):
  organisatie = models.CharField('Organisatie', max_length=100) 
  name        = models.CharField('Contactpersoon', max_length=100)
  adres       = models.CharField('Adres', max_length=100, blank=True)
  postcode    = models.CharField('Postcode', max_length=10, blank=True)
  plaats      = models.CharField('Plaats', max_length=100, blank=True)
  telefoon    = models.CharField('Telefoon', max_length=25)
  email       = models.EmailField('E-mail', max_length=100)
  # relaties
  rol         = models.ForeignKey(Rol, blank=True, null=True, on_delete=models.SET_NULL, related_name='contacten')
  # secundair
  uuid        = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at    = models.DateField('start at', auto_now=True, help_text='Start date of the contact record')
  end_at      = models.DateField('end at', blank=True, null=True, help_text='End date of the contact record')
  created     = models.DateTimeField(auto_now_add=True, help_text='Date when the contact was registered in the system')

  class Meta:
    verbose_name_plural = 'Contacten'

  def get_absolute_url(self):
    return reverse("show-contact", args=[self.uuid])

  # functie om contact in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.organisatie} - {self.name}'

# Domein model
class Domein(models.Model):
  url          = models.URLField('URL (SLD.TLD)', max_length=100)
  website      = models.BooleanField('Website', default=True)
  description  = models.TextField('Beschrijving', blank=True)
  opmerkingen  = models.TextField('Opmerkingen', blank=True)
  dnsipv4      = models.CharField('DNS record IPv4', blank=True, null=True, max_length=100)
  dnsipv6      = models.CharField('DNS record IPv6', blank=True, null=True, max_length=100)
  http         = models.BooleanField('http', default=False)
  https        = models.BooleanField('https', default=False)
  dnssec       = models.BooleanField('dnssec', default=False)
  spf          = models.BooleanField('spf', default=False)
  dmarc        = models.BooleanField('dmarc', default=False)
  sts          = models.BooleanField('sts', default=False)
  start        = models.DateField('Domein Start', blank=True, null=True)
  end          = models.DateField('Domein End', blank=True, null=True)
  slug         = models.SlugField(default= "", null=False)
  # relaties
  betrokkenen  = models.ManyToManyField(Contact, blank=True, related_name='domeinen')
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the domein record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the domein record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the Domein was registered in the system')

  class Meta:
    verbose_name_plural = 'domeinen'
  
  # method om te bepalen of domein nog geldig is
  @property
  def valid(self):
    today    = date.today()
    if self.end < today:
      valid = False
    else:
      valid = True
    return valid

  # method to calculate number of day til domeinregistratie expires
  @property
  def days_till_expiration(self):
    today = date.today()
    num_days = self.end - today
    num_days_stripped = str(num_days).split(',', 1)[0]
    return num_days_stripped

  # create absolute url to show domein
  def get_absolute_url(self):
    return reverse("show-domein", args=[self.uuid, self.slug])
  
  # override save method to add slug-field
  def save(self, *args, **kwargs):
    self.slug = slugify(self.url)
    super().save(*args, **kwargs)

  # functie om domein in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.url

# Subdomein model
class Subdomein(models.Model):
  url          = models.CharField('Subdomain', max_length=100)
  website      = models.BooleanField('Website', default=True)
  description  = models.TextField('Toelichting', blank=True)
  opmerkingen  = models.TextField('Opmerkingen', blank=True)
  dnsipv4      = models.CharField('DNS record IPv4', blank=True, null=True, max_length=100)
  dnsipv6      = models.CharField('DNS record IPv6', blank=True, null=True, max_length=100)
  http         = models.BooleanField('http', default=False)
  https        = models.BooleanField('https', default=False)
  dnssec       = models.BooleanField('dnssec', default=False)
  spf          = models.BooleanField('spf', default=False)
  dmarc        = models.BooleanField('dmarc', default=False)
  sts          = models.BooleanField('sts', default=False)
  start        = models.DateField('Subdomein Start', blank=True, null=True)
  end          = models.DateField('Subdomein End', blank=True, null=True)
  slug         = models.SlugField(default= "", null=False)
  # relaties
  domein       = models.ForeignKey(Domein, blank=True, null=True, on_delete=models.CASCADE, related_name='subdomeinen')
  betrokkenen  = models.ManyToManyField(Contact, blank=True, related_name='subdomeinen')
  # secundair  
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the subdomein record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the subdomein record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the Subdomein was registered in the system')

  class Meta:
    verbose_name_plural = 'subdomeinen'

  # method om te bepalen of subdomein nog geldig is
  @property
  def valid(self):
    today    = date.today()
    if self.end < today:
      valid = False
    else:
      valid = True
    return valid

  # method to calculate number of day til subdomeinregistratie expires
  @property
  def days_till_expiration(self):
    today = date.today()
    num_days = self.end - today
    num_days_stripped = str(num_days).split(',', 1)[0]
    return num_days_stripped

  # create absolute url to show subdomein
  def get_absolute_url(self):
    return reverse("show-subdomein", args=[self.uuid, self.slug])
  
  # override save method to add slug-field
  def save(self, *args, **kwargs):
    self.slug = slugify(self.url)
    super().save(*args, **kwargs)

  # functie om subdomein in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.url

# Certificaattype model
class Certificaattype(models.Model):
  type        = models.CharField('Certificaat type', max_length=100)
  description = models.TextField('Beschrijving', blank=True)
  # secundair
  uuid        = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  
  # functie om certificaattype in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f"{self.type}"

# Certificaat model
class Certificaat(models.Model):
  name         = models.CharField('Certificaatnaam', max_length=100)
  description  = models.TextField('Beschrijving', blank=True)
  opmerkingen  = models.TextField('Opmerkingen', blank=True)
  start        = models.DateField('Certificaat Start', blank=True, null=True)
  end          = models.DateField('Certificaat End', blank=True, null=True)
  # relaties
  type         = models.ForeignKey(Certificaattype, null=True, on_delete=models.SET_NULL, related_name='certificaten')
  domeinen     = models.ManyToManyField(Domein, blank=True, related_name='certificaten')
  subdomeinen  = models.ManyToManyField(Subdomein, blank=True, related_name='certificaten')
  servers      = models.ManyToManyField(Server, blank=True, related_name='certificaten')
  services     = models.ManyToManyField(Service, blank=True, related_name='certificaten')
  betrokkenen  = models.ManyToManyField(Contact, blank=True, related_name='certificaten')
  # secundair
  uuid         = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at     = models.DateField('start at', auto_now=True, help_text='Start date of the certificaat record')
  end_at       = models.DateField('end at', editable=False, blank=True, null=True, help_text='End date of the certificaat record')
  created      = models.DateTimeField(auto_now_add=True, help_text='Date when the certificaat was registered in the system')

  class Meta:
    ordering = ['name']
    verbose_name_plural = 'certificaten'
  
  # method om te bepalen of certificaat nog geldig is
  @property
  def valid(self):
    today    = date.today()
    if self.end < today:
      valid = False
    else:
      valid = True
    return valid

  # method to calculate number of day til certificaatregistratie expires
  @property
  def days_till_expiration(self):
    today = date.today()
    num_days = self.end - today
    num_days_stripped = str(num_days).split(',', 1)[0]
    return num_days_stripped
    
  # create absolute url to show certificaat
  def get_absolute_url(self):
    return reverse("show-certificaat", args=[self.uuid])
  
  # functie om certificaat in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.name} - {self.type}'
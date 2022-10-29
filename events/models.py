# events/models.py

import uuid

# Django
#from djgeojson.fields import PointsField
from django.db import models
from django.db.models.base import Model
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from django.utils.html import mark_safe
#from django.contrib.gis.db.models import GeometryField
from datetime import date

# Venue model
class Venue(models.Model):
  index     = models.PositiveIntegerField(default=1, help_text='Incremental index number of the venue record.')
  name      = models.CharField('Naam', max_length=255)
  adres     = models.CharField(max_length=255)
  postcode  = models.CharField('Postcode', max_length=10)
  plaats    = models.CharField('Plaats', max_length=100)
  telefoon  = models.CharField('Telefoon', max_length=25, blank=True)
  website   = models.URLField('Website', max_length=100, blank=True)
  email     = models.EmailField('E-mail', max_length=100, blank=True)
  image     = models.ImageField(upload_to='images/events/', blank=True, null=True)
  #relaties
  owner     = models.IntegerField("Owner", blank=False)
  # secundair
  uuid      = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  start_at  = models.DateField('start at', auto_now=True, help_text='Start date of the venue record')
  end_at    = models.DateField('end at', blank=True, null=True, help_text='End date of the venue record')
  created   = models.DateTimeField(auto_now_add=True, help_text='Date when the Venue was registered in the system')

  # method om model in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.name}'
  # method om image in de admin web-pagina te kunnen presenteren
  def image_tag(self):
    if self.image != '':
      return mark_safe('<img src="%s%s" height="100" />' % (f'{settings.MEDIA_URL}', self.image))

# Visitor model
class Visitor(models.Model):
  first_name = models.CharField('Visitor FirstName', max_length=100)
  last_name  = models.CharField('Visitor LastName', max_length=100)
  telefoon   = models.CharField('Visitor Telefoon', max_length=25)
  email      = models.EmailField('Visitor Email', max_length=100)

  # functie om visitor in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.first_name + ' ' + self.last_name

# Event model
class Event(models.Model):
  name        = models.CharField('Event Name', max_length=255, help_text='Name of the event')
  description = models.TextField('Event Description', blank=True, help_text='Description of the event')
  slug        = models.SlugField(default= "", null=False)
  event_start = models.DateTimeField('Event Start', blank=True)
  event_end   = models.DateTimeField('Event End', blank=True)
  approved    = models.BooleanField('Approved', default=False)
  # relaties
  venue       = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE, related_name='events', help_text='Venue this event takes place')
  manager     = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, help_text='Manager of the event')
  attendees   = models.ManyToManyField(Visitor, blank=True)
  # secundair
  uuid        = models.UUIDField(unique=True, default=uuid.uuid4, help_text='Unique identifier (UUID4)')
  created     = models.DateTimeField(auto_now_add=True, help_text='Date when the Event was created')
 
  # method om te bepalen of event al is geweest
  @property
  def timing(self):
    today    = date.today()
    if self.event_start.date() < today:
      moment = 'verleden'
    elif self.event_start.date() > today:
      moment = 'toekomst'
    else:
      moment = 'vandaag'
    return moment

  # method to calculate number of day til event starts
  @property
  def days_till(self):
    today    = date.today()
    num_days = self.event_start.date() - today
    num_days_stripped = str(num_days).split(',', 1)[0]
    return num_days_stripped

  # method to event with edit url
  @property
  def get_html_url(self):
    url = reverse('edit_event', args=(self.id,))
    return f'<a href="{url}"> {self.name} </a>'

  # override save method to add slug-field
  def save(self, *args, **kwargs):
    self.slug = slugify(self.name)
    super().save(*args, **kwargs)

  # functie om event in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return self.name

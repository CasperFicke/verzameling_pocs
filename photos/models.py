# fotos/models.py

from typing import Any
from django.db import models
from django.conf import settings
from django.utils.html import mark_safe

# Create your models here.
class Photo(models.Model):
  name        = models.CharField(max_length=100)
  description = models.TextField()
  image       = models.ImageField(upload_to= 'images/photos/')
  created     = models.DateTimeField(auto_now_add=True)

  # functie om object in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f'{self.name}'
  # functie om image in de admin web-pagina te kunnen presenteren
  def image_tag(self):
    if self.image != '':
      return mark_safe('<img src="%s%s" width="100" height="100" />' % (f'{settings.MEDIA_URL}', self.image))
  # override delete method to also delete the image
  def delete(self):
    self.image.delete()
    super().delete()
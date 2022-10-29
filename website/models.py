### MODELS.PY WEBSITE APP ###

# Django
from django.db import models

# Course model
class Course(models.Model):
  name     = models.CharField(max_length=100)
  language = models.CharField(max_length=100)
  price    = models.CharField(max_length=20)

  # register model in admin area
  def __str__(self):
    return self.name

# stocks/models.py

# Django
from django.db import models

#these are model abstracts from django extensions
from django_extensions.db.models import (
  TimeStampedModel,
	ActivatorModel 
)

# Stock model
class Stock(TimeStampedModel, ActivatorModel, models.Model):
  ticker_name        = models.CharField(max_length=10)
  ticker_description = models.CharField(max_length=200, default="")

  class Meta:
        ordering = ('ticker_name',)

  # register model in admin area
  def __str__(self):
    return self.ticker_name

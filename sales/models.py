### sales/admin.py ###

# Django
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField

from django.contrib.auth.models import User

# Create your models here.
PRODUCT_CHOISES = (
  ('TV', 'tv'),
  ('IPAD', 'ipad'),
  ('PLAYSTATION', 'playstation'),
)

# Sale model
class Sale(models.Model):
  product  = models.CharField(max_length=50, choices=PRODUCT_CHOISES)
  salesman = models.ForeignKey(User, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  total    = models.FloatField(blank=True)
  created  = models.DateTimeField(auto_now_add=True)
  updated  = models.DateTimeField(auto_now=True)

  # functie om Sales in de admin web-pagina te kunnen presenteren
  def __str__(self):
    return f"{self.product} - {self.quantity}"
  
  # override save-method
  def save(self, *args, **kwargs):
    price = None
    if self.product == 'TV':
      price = 400
    elif self.product == 'IPAD':
      price = 500
    elif self.product == 'PLAYSTATION':
      price = 600
    else:
      pass
    self.total = price * self.quantity
    super().save(*args, **kwargs)

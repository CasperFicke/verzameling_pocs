# maps/signals.py

from django.db.models.signals import post_save
from .models import Plaats
from django.dispatch import receiver

# na save van plaats 
@receiver(post_save, sender=Plaats)
def printplaats(sender, instance, created, **kwargs):
  print(instance.naam)
  print(instance.latitude)
  print(instance.longitude)

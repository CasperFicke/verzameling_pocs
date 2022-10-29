# users/signals.py
""""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile
from django.dispatch import receiver

# na save van user create userprofile
@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

# na save van user save userprofile
@receiver(post_save, sender=User)
def save_userprofile(sender, instance, **kwargs):
  instance.userprofile.save()
"""
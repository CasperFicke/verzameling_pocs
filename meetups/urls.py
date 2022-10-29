# meetups/urls.py

# Django
from django.urls import path

# local
from . import views

urlpatterns = [
  # Meetups
  path('meetups/'            , views.index_meetups, name="index-meetups"),
  path('meetups/all_meetups/' , views.all_meetups, name="all-meetups"),
  path('meetups/<slug:meetup_slug>/' , views.show_meetup, name="show-meetup")
]


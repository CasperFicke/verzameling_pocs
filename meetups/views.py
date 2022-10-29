# meetups/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404

from .models import Meetup

# Meetups indexpage view
def index_meetups(request):
  title = 'index meetups'
  context = {
    'title': title
  }
  return render(request, 'meetups/index_meetups.html', context)

# All meetups view  
def all_meetups(request):
  title = 'all meetups'
  meetups = Meetup.objects.all()
  context = {
    'title': title,
    'show_meetups': True,
    'meetups': meetups
  }
  return render(request, 'meetups/all_meetups.html', context)

# Show meetup
def show_meetup(request, meetup_slug):
  try:
    meetup  = Meetup.objects.get(slug=meetup_slug)
    title   = meetup.title
    context = {
      'title'  : title,
      'meetup' : meetup,
      'meetup_found' : True
    }
    return render(request, 'meetups/show_meetup.html', context)
  except:
    context = {
      'meetup_found' : False
    }
    return render(request, 'meetups/show_meetup.html', context)
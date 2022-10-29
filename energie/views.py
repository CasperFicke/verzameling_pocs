# energie/views.py

# Django
from django.core.paginator import Paginator
from django.shortcuts import render

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import io
import urllib, base64

# Local
from .models import Meterstand, Meter

from datetime import datetime, timedelta

# Enegie indexpage
def energie_index(request):
  title = 'energie indexpage'
  context ={
    'title': title
  }
  return render(request, 'energie/energie_index.html', context)

# All Meterstanden view (function based)
# (/meterstanden/ is standen van alle meters, /meterstanden/medium/ is meterstanden van ingevoerd medium)
def all_meterstanden(request, energietype='alle'):
  meterstanden_list = Meterstand.objects.all()
  # select standen van een gekozen medium
  medium_list = []
  medium = ''
  if energietype != 'alle':
    for item in meterstanden_list:
      if item.meter.medium.energietype.name == energietype:
        medium_list.append(item)
        medium = item.meter.medium.name
    meterstanden_list = medium_list
  sorted_list = sorted(meterstanden_list, key=lambda meterstand: meterstand.meterstand_date, reverse=False)
  dates_list = []
  value_list = []
  for item in sorted_list:
    dates_list.append(item.meterstand_date)
    value_list.append(item.meterstand_waarde)
  # define axes for the plot
  x = dates_list
  y = value_list

  # set firstletter of medium to uppercase
  energietype = energietype.capitalize()

  fig, ax = plt.subplots()
  fig.suptitle(energietype)
  # (1, 1, 1) staat voor lokatie van de figuur op het werkblad; (aantal rijen, aantal kolommen, plaats van het figuur)
  #axes = figure.add_subplot(1, 1, 1)
  #axes.set_ylim(0,100)
  ax.set_xlabel('datum')
  #ax.set_ylabel(meter.eenheid)
  # format date on X-axis
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
  # set interval to 3 month on x-axis
  plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
  
  # plot graph
  ax.plot(x,y, 'tab:orange', label=energietype)
  # rotates and right aligns the x labels, and moves the bottom of the axes up to make room for them
  fig.autofmt_xdate()
  plt.legend()

  # convert graph into string buffer and then we convert 64 bit code into image
  buf = io.BytesIO()
  fig.savefig(buf,format='png')
  buf.seek(0)
  string = base64.b64encode(buf.read())
  uri =  urllib.parse.quote(string)

  # pagination
  paginator          = Paginator(sorted_list, 20) # Show 20 meterstanden per page.
  page_number        = request.GET.get('page')
  meterstanden_page  = paginator.get_page(page_number)
  page_count         = "a" * meterstanden_page.paginator.num_pages
  is_paginated       = meterstanden_page.has_other_pages
  meterstanden_count = len(sorted_list)
  context = {
    'aantal'       : meterstanden_count,
    'page_obj'     : meterstanden_page,
    'is_paginated' : is_paginated,
    'page_count'   : page_count,
    'medium'       : medium,
    'energietype'  : energietype,
    'data'         : uri,
  }
  return render(request, 'energie/all_meterstanden.html', context)
  # return  render(request, 'all_meterstanden.html', {'meterstanden_list': meterstanden_list})

# All electriciteitsmeters view (function based)
def all_electriciteit(request):
  # maak list met alle meterstanden
  meterstanden_list = Meterstand.objects.all()
  # maak lege list per te presenteren meterstandenlijst
  panelen_list=[]
  teruglaag_list=[]
  terughoog_list=[]
  ingekochtlaag_list=[]
  ingekochthoog_list=[]
  # vul voor iedere meter de standenlijst
  for item in meterstanden_list:
    if item.meter.medium.name == 'zonnepanelen':
      panelen_list.append(item)
    elif item.meter.medium.name == 'Teruggeleverd Laagtarief':
      teruglaag_list.append(item)
    elif item.meter.medium.name == 'Teruggeleverd Hoogtarief':
      terughoog_list.append(item)
    elif item.meter.medium.name == 'Ingekocht Laagtarief':
      ingekochtlaag_list.append(item)
    elif item.meter.medium.name == 'Ingekocht Hoogtarief':
      ingekochthoog_list.append(item)

    #meterstanden_list = panelen_list
  # sorteer meterstanden op datum
  pan_sorted_list = sorted(panelen_list, key=lambda meterstand: meterstand.meterstand_date, reverse=False)
  tl_sorted_list  = sorted(teruglaag_list, key=lambda meterstand: meterstand.meterstand_date, reverse=False)
  th_sorted_list  = sorted(terughoog_list, key=lambda meterstand: meterstand.meterstand_date, reverse=False)
  il_sorted_list  = sorted(ingekochtlaag_list, key=lambda meterstand: meterstand.meterstand_date, reverse=False)
  ih_sorted_list  = sorted(ingekochthoog_list, key=lambda meterstand: meterstand.meterstand_date, reverse=False)
  # maak lege list per te presenteren meterstandenlijst
  dates_list = []
  pan_list   = []
  tl_list    = []
  th_list    = []
  il_list    = []
  ih_list    = []
  # vul voor iedere meter de standenlijst
  for item in pan_sorted_list:
    dates_list.append(item.meterstand_date)
    pan_list.append(item.meterstand_waarde)
  for item in tl_sorted_list:
    tl_list.append(item.meterstand_waarde)
  for item in th_sorted_list:
    th_list.append(item.meterstand_waarde)
  for item in il_sorted_list:
    il_list.append(item.meterstand_waarde)
  for item in ih_sorted_list:
    ih_list.append(item.meterstand_waarde)
  # define axes for the plot
  x = dates_list
  pan = pan_list
  tl  = tl_list
  th  = th_list
  il  = il_list
  ih  = ih_list

  fig, ax = plt.subplots()
  fig.suptitle('electriciteitsmeters')
  # (1, 1, 1) staat voor lokatie van de figuur op het werkblad; (aantal rijen, aantal kolommen, plaats van het figuur)
  #axes = figure.add_subplot(1, 1, 1)
  #axes.set_ylim(0,100)
  ax.set_xlabel('datum')
  ax.set_ylabel('meterstand (kWh)')
  # format date on X-axis
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
  # set interval to 3 month on x-axis
  plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
  
  # plot graph
  ax.plot(x,pan, 'tab:orange', label='panelen')
  ax.plot(x,tl,  'tab:green' , label='terug-laag')
  ax.plot(x,th,  'tab:blue'  , label='terug-hoog')
  ax.plot(x,il,  'tab:gray'  , label='gekocht-laag')
  ax.plot(x,ih,  'tab:red'   , label='gekocht-hoog')
  # rotates and right aligns the x labels, and moves the bottom of the axes up to make room for them
  fig.autofmt_xdate()
  # zet legenda in de grafiek
  plt.legend()

  # convert graph into string buffer and then convert base64 code into image
  buf = io.BytesIO()
  fig.savefig(buf, format='png')
  buf.seek(0)
  string = base64.b64encode(buf.read())
  uri    = urllib.parse.quote(string)

  context = {
    'data' : uri,
  }
  return render(request, 'energie/all_electriciteit.html', context)
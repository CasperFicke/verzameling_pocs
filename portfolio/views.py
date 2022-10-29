# portfolio/views.py

# django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.views import generic

import json
import requests
import os

import folium
from folium import plugins

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="meteo")

# local
from .models import (
  UserProfileP,
  Testimonial,
  ContactProfile,
  Portfolio,
  Blog,
  Certificate
)
from . forms import ContactForm

# Portfolio homepage
def home_portfolio(request):
  title   = 'home portfolio'
  context = {
    'title': title
  }
  return render(request, 'portfolio/home_portfolio.html', context)

# PortfolioIndex view
class IndexView(generic.TemplateView):
	template_name = "portfolio/index_portfolio.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		testimonials = Testimonial.objects.filter(is_active=True)
		certificates = Certificate.objects.filter(is_active=True)
		blogs        = Blog.objects.filter(is_active=True)
		portfolio    = Portfolio.objects.filter(is_active=True)
		
		context["testimonials"] = testimonials
		context["certificates"] = certificates
		context["blogs"]        = blogs
		context["portfolio"]    = portfolio
		return context

# Contact view
class ContactView(generic.FormView):
  model = ContactProfile
  template_name = "portfolio/contact.html"
  form_class    = ContactForm
  success_url   = "/"

  def form_valid(self, form):
    form.save()
    messages.success(self.request, 'Thank you. We will be in touch soon.')
    return super().form_valid(form)

# Portfolio view
class PortfolioView(generic.ListView):
	model         = Portfolio
	template_name = "portfolio/portfolio.html"
	paginate_by   = 10

	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)

# Portfoliodetail view
class PortfolioDetailView(generic.DetailView):
	model         = Portfolio
	template_name = "portfolio/portfolio_detail.html"

# Blog view
class BlogView(generic.ListView):
	model         = Blog
	template_name = "portfolio/blog.html"
	paginate_by   = 10
	
	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)

# Blogdetail view
class BlogDetailView(generic.DetailView):
	model         = Blog
	template_name = "portfolio/blog_detail.html"


# Meteo indexpage
def index_meteo(request):
  title = 'index meteo'
  context = {
    'title': title
  }
  return render(request, 'portfolio/index_meteo.html', context)

# getij view
def getij(request):
  title = 'getij'
  meteoserver_apikey = os.getenv('METEOSERVER_APIKEY')
  if request.method == "POST":
    lokatie_ = request.POST['lokatie']
    lokatie = geolocator.geocode(lokatie_)
    if lokatie == None:
      return HttpResponse( 'location input is invalid')
    loc_name  = lokatie
    loc_lat   = lokatie.latitude
    loc_lon   = lokatie.longitude
    loc_point = (loc_lat, loc_lon)
    url    = 'https://data.meteoserver.nl/api/getij.php'
    params = {
      'lat'  : loc_lat,
      'long' : loc_lon,
      'key'  : meteoserver_apikey
    }
    headers = {}
    api_request = requests.get(url, params)
    try:
      standenlijst = []
      api_result = json.loads(api_request.content)
      standenlijst = api_result['jsongetij'][1]['tijden']
    except Exception as e:
      api_result = "Error..."
    # kaart
    tooltip = 'Click voor meer info'
    popup   = lokatie
    m = folium.Map(
      location   = (params['lat'], params['long']),
      zoom_start = 8
    )
    # add lokatie to map
    folium.Marker(
        location = (params['lat'], params['long']),
        popup    = popup,
        tooltip  = tooltip,
        #icon = folium.Icon(color=mc, prefix='fa', icon=mi)
      ).add_to(m)
    m = m._repr_html_()
    
    context = {
      'title'        : title,
      'api_result'   : api_result,
      'standenlijst' : standenlijst,
      'm'            : m
    }
    return render(request, 'portfolio/getij.html', context)   

# weer view
def weer(request):
  title = 'weerbericht'
  meteoserver_apikey = os.getenv('METEOSERVER_APIKEY')
  if request.method == "POST":
    lokatie_ = request.POST['lokatie']
    lokatie = geolocator.geocode(lokatie_)
    if lokatie == None:
      return HttpResponse( 'location input is invalid')
    loc_name  = lokatie
    loc_lat   = lokatie.latitude
    loc_lon   = lokatie.longitude
    loc_point = (loc_lat, loc_lon)
    url    = 'https://data.meteoserver.nl/api/zeeweer.php'
    params = {
      'lat'  : loc_lat,
      'long' : loc_lon,
      'key'  : meteoserver_apikey
    }
    headers = {}
    api_request = requests.get(url, params)
  lokatie = ''
  try:
    getijlijst = []
    api_result = json.loads(api_request.content)
    lokatie    = api_result['liveweer'][0]['plaats']
    getijlijst = api_result['getij']
  except Exception as e:
    api_result = "Error..."
  # kaart
  tooltip = 'Click voor meer info'
  popup   = lokatie
  m = folium.Map(
    location   = (params['lat'], params['long']),
    zoom_start = 8
  )
  # add lokatie to map
  folium.Marker(
      location = (params['lat'], params['long']),
      popup    = popup,
      tooltip  = tooltip,
      #icon = folium.Icon(color=mc, prefix='fa', icon=mi)
    ).add_to(m)
  m = m._repr_html_()
  context = {
    'title'      : title,
    'api_result' : api_result,
    'getijlijst' : getijlijst,
    'm'          : m
  }
  return render(request, 'portfolio/weer.html', context)

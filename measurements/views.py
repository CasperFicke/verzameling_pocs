# measurements/views.py

# django
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404

from geopy.geocoders import Nominatim
from geopy.distance  import geodesic
from geographiclib.geodesic import Geodesic

#import math

geod = Geodesic.WGS84

import folium

# local
from .models import Measurement, Endpoint
from .forms import MeasurementForm, EndpointForm
from .utils import get_ip_address, get_center_coords, get_zoom

# All measurements
def calculate_distance(request):
  title    = 'Afstanden'
  metingen = Measurement.objects.all()
  # Initial folium map
  startcenter = [52, 5]
  m = folium.Map(
    location   = get_center_coords(startcenter[0], startcenter[1]),
    zoom_start = 6,
  )
  form  = MeasurementForm(request.POST or None)
  geolocator = Nominatim(user_agent='measurements')

  ip_ = get_ip_address(request)
  # print (ip_)

  if form.is_valid():
    instance = form.save(commit=False) # dont save yet
    # get location data
    location_ = form.cleaned_data.get('location')
    location  = geolocator.geocode(location_)
    if location == None:
      return HttpResponse( 'location input is invalid')
    loc_name  = location
    loc_lat   = location.latitude
    loc_lon   = location.longitude
    loc_point = (loc_lat, loc_lon)
    #get destination data
    destination_ = form.cleaned_data.get('destination')
    destination  = geolocator.geocode(destination_)
    if location == None or destination == None:
     return HttpResponse( 'destination input is invalid')
    des_name  = destination
    des_lat   = destination.latitude
    des_lon   = destination.longitude
    des_point = (des_lat, des_lon)
    # calculate distance
    dist_km = round(geodesic(loc_point, des_point).km, 2)
    dist_nm = round(dist_km/1.852, 2)
    instance.dist_km = dist_km
    instance.dist_nm = dist_nm
    dist_popup = f'{dist_km} km, {dist_nm} mijl'
    # calculate bearing
    g = geod.Inverse(loc_lat, loc_lon, des_lat, des_lon)
    ri =  g['azi1']
    if ri < 0:
      ri += 360
    instance.bearing = round(ri, 1)
    # save
    instance.save()

    # folium map modifications
    center = get_center_coords(loc_lat, loc_lon, des_lat, des_lon) # helperfunction uit utils.py
    m = folium.Map(
      location   = center,
      zoom_start = get_zoom(dist_km), # helperfunction uit utils.py
    )
    # add location marker
    folium.Marker(
      [loc_lat, loc_lon],
      tooltip = 'click for more',
      popup   = location,
      icon    = folium.Icon(color='blue')
    ).add_to(m)
    # add destination marker
    folium.Marker(
      [des_lat, des_lon],
      tooltip = 'click for more',
      popup   = destination,
      icon    = folium.Icon(color='purple')
    ).add_to(m)
    # draw line
    line = folium.PolyLine(
      locations = [loc_point, des_point],
      tooltip   = 'click for more',
      popup     = dist_popup,
      weight    = 2,
      color     = 'blue')
    m.add_child(line)
  # maak html representatie van de kaart
  m = m._repr_html_()

  context = {
    'title'    : title,
    'metingen' : metingen,
    #'distance' : obj,
    'form'     : form,
    'map'      : m,
  }
  return render(request, 'measurements/afstand.html', context)

# Show mesurement
def show_measurement(request, measurement_uuid):
  title      = 'Afstand'
  meting     = Measurement.objects.get(uuid = measurement_uuid)
  t_tip      = 'click for more'
  dist_popup = f'{meting.dist_km} km, {meting.dist_nm} mijl, {meting.bearing} °'
  geolocator = Nominatim(user_agent='measurements')
  # get location data
  location_ = meting.location
  location  = geolocator.geocode(location_)
  loc_lat   = location.latitude
  loc_lon   = location.longitude
  loc_point = (loc_lat, loc_lon)
  #get destination data
  destination_ = meting.destination
  destination  = geolocator.geocode(destination_)
  des_lat      = destination.latitude
  des_lon      = destination.longitude
  des_point    = (des_lat, des_lon)

  # folium map
  center = get_center_coords(loc_lat, loc_lon, des_lat, des_lon)
  m = folium.Map(
    location=center,
    zoom_start=get_zoom(meting.dist_km),
  )
  
  # add layer for circle and line
  shapesLayer = folium.FeatureGroup(name="info").add_to(m)

  # add location marker
  folium.Marker(
    [loc_lat, loc_lon],
    tooltip = 'click for more',
    popup   = folium.Popup(f'<h2>{meting.location}</h2><br/>This is a <b>new line</b><br/><img src="https://www.w3schools.com/html/pic_trulli.jpg" alt="Trulli" style="max-width:100%;max-height:100%">', max_width=400),
    icon    = folium.Icon(color='blue')
  ).add_to(m)
  # add destination marker
  folium.Marker(
    [des_lat, des_lon],
    tooltip = t_tip,
    popup   = folium.Popup(f'<h2>{meting.destination}</h2><br/>This is a <b>new line</b><br/><img src="https://www.w3schools.com/html/pic_trulli.jpg" alt="Trulli" style="max-width:100%;max-height:100%">', max_width=400),
    icon    = folium.Icon(color='purple')
  ).add_to(m)
  # add scaling circle
  folium.Circle(location=[loc_lat, loc_lon],
    radius = float(meting.dist_km*1000),
    fill=True,
    #tooltip = t_tip,
    #popup=folium.Popup(f'De <b>Afstand</b> is:<br/><h3>{dist_popup}</h3>', max_width=400)
  ).add_to(shapesLayer)
  # draw line
  line = folium.PolyLine(
    locations = [loc_point, des_point],
    tooltip   = t_tip,
    popup=folium.Popup(f'Van {meting.location} naar {meting.destination}:<br/><h3>{dist_popup}</h3>', max_width=400),
    weight    = 2,
    color     = 'blue')
  shapesLayer.add_child(line)
  
  # layercontrol
  folium.LayerControl(collapsed=False).add_to(m)
  # maak kaart 
  m = m._repr_html_()
  context = {
    'title'  : title,
    'meting' : meting,
    'map'    : m,
  }
  return render(request, 'measurements/show_measurement.html', context)

# All endpoints
def calculate_endpoint(request):
  title     = 'endpoints'
  endpoints = Endpoint.objects.all()
  # Initial folium map
  startcenter = [52, 5]
  m = folium.Map(
    location   = get_center_coords(startcenter[0], startcenter[1]),
    zoom_start = 6,
  )
  form       = EndpointForm(request.POST or None)
  geolocator = Nominatim(user_agent='measurements')

  if form.is_valid():
    instance = form.save(commit=False) # dont save yet
    # get location data
    location_ = form.cleaned_data.get('location')
    location  = geolocator.geocode(location_)
    if location == None:
      return HttpResponse( 'location input is invalid')
    loc_name  = location
    loc_lat   = location.latitude
    loc_lon   = location.longitude
    loc_point = (loc_lat, loc_lon)
    # calc destination on bearing and distance
    bearing   = form.cleaned_data.get('bearing')
    dist_km   = form.cleaned_data.get('dist_km')
    dist_m    = dist_km*1000
    #dist_nm    = dist_km/1.852
    g = geod.Direct(loc_lat, loc_lon, bearing, float(dist_m))
    des_lat   = g['lat2']
    des_lon   = g['lon2']
    des_point = (des_lat, des_lon)
    
    # save
    instance.save()

    # folium map modifications
    center = get_center_coords(loc_lat, loc_lon, des_lat, des_lon) # helperfunction uit utils.py
    m = folium.Map(
      location   = center,
      zoom_start = get_zoom(dist_km), # helperfunction uit utils.py
    )
    # add location marker
    folium.Marker(
      [loc_lat, loc_lon],
      tooltip = 'click for more',
      popup   = location,
      icon    = folium.Icon(color='blue')
    ).add_to(m)
    # add destination marker
    folium.Marker(
      [des_lat, des_lon],
      tooltip = 'click for more',
      #popup   = destination,
      icon    = folium.Icon(color='purple')
    ).add_to(m)
    # draw line
    line = folium.PolyLine(
      locations = [loc_point, des_point],
      tooltip   = 'click for more',
      #popup     = dist_popup,
      weight    = 2,
      color     = 'blue')
    m.add_child(line)
  # maak html representatie van de kaart
  m = m._repr_html_()

  context = {
    'title'     : title,
    'endpoints' : endpoints,
    #'distance' : obj,
    'form'      : form,
    'map'       : m,
  }
  return render(request, 'measurements/endpoint.html', context)

# Show endpoint
def show_endpoint(request, endpoint_uuid):
  title      = 'endpoint'
  endpoint   = Endpoint.objects.get(uuid = endpoint_uuid)
  bearing    = endpoint.bearing
  dist_km    = endpoint.dist_km
  dist_nm    = endpoint.dist_nm
  line_popup = f'{endpoint.dist_km} km, {endpoint.dist_nm} mijl, {endpoint.bearing} °'
  geolocator = Nominatim(user_agent='measurements')
  # get location data
  location_ = endpoint.location
  location  = geolocator.geocode(location_)
  loc_name  = location
  loc_lat   = location.latitude
  loc_lon   = location.longitude
  loc_point = (loc_lat, loc_lon)
  # calc destination on bearing and distance
  g = geod.Direct(loc_lat, loc_lon, bearing, float(dist_km)*1000)
  des_lat    = g['lat2']
  des_lon    = g['lon2']
  des_point  = (des_lat, des_lon)
  # folium map
  center = get_center_coords(loc_lat, loc_lon, des_lat, des_lon)
  m = folium.Map(
    location=center,
    zoom_start=get_zoom(endpoint.dist_km),
  )

  t_tip = 'click for more'
  # add location marker
  folium.Marker(
    [loc_lat, loc_lon],
    tooltip = 'click for more',
    popup   = folium.Popup(f'<h2>{endpoint.location}</h2><br/>This is a <b>new line</b><br/><img src="https://www.w3schools.com/html/pic_trulli.jpg" alt="Trulli" style="max-width:100%;max-height:100%">', max_width=400),
    icon    = folium.Icon(color='blue')
  ).add_to(m)
  # draw line
  line = folium.PolyLine(
    locations = [loc_point, des_point],
    tooltip   = t_tip,
    popup=folium.Popup(f'De <b>Afstand</b> is:<br/><h3>{line_popup}</h3>', max_width=400),
    weight    = 2,
    color     = 'blue')
  m.add_child(line)
  # add endpoint marker
  folium.Marker(
    [g['lat2'],g['lon2']],
    tooltip = 'click for more',
    popup   = [g['lat2'],g['lon2']],
    icon    = folium.Icon(color='purple')
  ).add_to(m)
  # maak kaart 
  m = m._repr_html_()
  
  context = {
    'title'     : title,
    'endpoint'  : endpoint,
    'des_point' : des_point,
    'map'       : m,
  }
  return render(request, 'measurements/show_endpoint.html', context)


# measurements.utils.py

from django.contrib.gis.geoip2 import GeoIP2

# helper functions

# get ip adres
def get_ip_address(request):
  x_forwarded_for =request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip

# get geo data voor een IP adres
def get_geo(ip):
  g        = GeoIP2()
  country  = g.country(ip)
  city     = g.city(ip)
  lat, lon = g.lat_lon(ip)
  return country, city, lat, lon

# bepaal center
def get_center_coords(latA, lonA, latB=None, lonB=None):
  cord = (latA, lonA)
  if latB:
    cord = [(latA+latB)/2, (lonA+lonB)/2]
  return cord

# bepaal zoom
def get_zoom(distance):
  if distance <= 100:
    return 8
  elif distance > 100 and distance <= 2000:
    return 6
  elif distance > 2000 and distance <= 5000:
    return 4
  else:
    return 2
  

# measurements/urls.py

# Django
from django.urls import path

# local
from . import views

#app_name = 'measurements'

urlpatterns = [
  # Measurements
  path('measurements/afstand/'                   , views.calculate_distance, name='calculate-distance'),
  path('measurements/afstand/<measurement_uuid>/', views.show_measurement, name='show-measurement'),
  path('measurements/endpoint/'                  , views.calculate_endpoint, name='calculate-endpoint'),
  path('measurements/endpoint/<endpoint_uuid>/'  , views.show_endpoint, name='show-endpoint'),
  ]
# energie/urls.py

# Django
from django.urls import path, include

# local
from . import views

urlpatterns = [
  # METERSTANDEN
  path('energie/'                          , views.energie_index, name="energie-index"),
  path('energie/meterstanden/'             , views.all_meterstanden, name="all-meterstanden"),
  path('energie/meterstanden/electriciteit' , views.all_electriciteit, name="all-electriciteit"),
  path('energie/meterstanden/<str:energietype>/', views.all_meterstanden , name="all-meterstanden"), # path converter
]

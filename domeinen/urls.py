# domeinen/urls.py

# Django
from django.urls import path

# local
from . import views

urlpatterns = [
  # Domeinen
  path('domeinen/index/' , views.domeinen_index, name="domeinen-index"),
  path('domeinen/'       , views.all_domeinen, name="all-domeinen"),
  path('domeinen/csv/'   , views.csv_domeinen, name="csv-domeinen"),
  path('domeinen/add/'   , views.add_domein, name="add-domein"),
  path('domeinen/<domein_uuid>/<slug:domein_slug>/'       , views.show_domein, name="show-domein"),
  path('domeinen/<domein_uuid>/<slug:domein_slug>/edit/'  , views.edit_domein, name="edit-domein"),
  path('domeinen/<domein_uuid>/<slug:domein_slug>/delete/', views.delete_domein, name="delete-domein"),

  # Subdomeinen
  path('domeinen/subdomeinen/'     , views.all_subdomeinen, name="all-subdomeinen"),
  #path('domeinen/subdomeinen/add/', views.add_subdomein, name="add-subdomein"),
  path('domeinen/subdomeinen/<subdomein_uuid>/<slug:subdomein_slug>/'       , views.show_subdomein, name="show-subdomein"),
  path('domeinen/subdomeinen/<subdomein_uuid>/<slug:subdomein_slug>/edit/'  , views.edit_subdomein, name="edit-subdomein"),
  path('domeinen/subdomeinen/<subdomein_uuid>/<slug:subdomein_slug>/delete/', views.delete_subdomein, name="delete-subdomein"),

  # Certificaten
  path('certificaten/'                   , views.all_certificaten, name="all-certificaten"),
  path('certificaten/<certificaat_uuid>/', views.show_certificaat, name="show-certificaat"),

  # Servers
  path('servers/'              , views.all_servers, name="all-servers"),
  path('servers/<server_uuid>' , views.show_server, name="show-server"),
  
  # Services
  path('servers/services/'               , views.all_services, name="all-services"),
  path('servers/services/<service_uuid>' , views.show_service, name="show-service"),

  # Contacten
  path('contacten/'                      , views.all_contacten, name="all-contacten"),
  path('contacten/add/'                  , views.add_contact, name="add-contact"),
  path('contacten/<contact_uuid>/'       , views.show_contact, name="show-contact"),
  path('contacten/<contact_uuid>/edit/'  , views.edit_contact, name="edit-contact"),
  path('contacten/<contact_uuid>/delete/', views.delete_contact, name="delete-contact"),

  # Rollen api-urls
  path('api/rollen/apis/'              , views.rollen_apis, name="rollen-apis"),
  path('api/rollen/'                   , views.rolList, name="rol-list"),
  path('api/rollen/add/'               , views.rolCreate, name="rol-create"),
  path('api/rollen/<str:rol_uuid>/'        , views.rolDetail, name="rol-detail"),
  path('api/rollen/<str:rol_uuid>/edit/'   , views.rolUpdate, name="rol-update"),
  path('api/rollen/<str:rol_uuid>/delete/' , views.rolDelete, name="rol-delete"),
]

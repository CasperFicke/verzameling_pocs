# maps/urls.py

# Django
from django.urls import path

# local
from . import views

app_name = "maps"

urlpatterns = [
  # Google maps
  path('maps/googlebasis/'  , views.google_basis, name="google-basis"),
  path('maps/googleroute/'  , views.google_route, name="google-route"),
  path('maps/googlemap/'    , views.google_map, name="google-map"),
  # MAPS
  path('maps/map/'               , views.default_map, name="default_map"), # mapbox
  path('maps/basiskaart/'        , views.basiskaart, name="basiskaart"),
  path('maps/openlayerskaart/'   , views.openlayerskaart, name="openlayerskaart"),
  path('maps/zwemkaart/'         , views.zwemkaart, name="zwemkaart"),
  path('maps/unemploymentkaart/' , views.unemploymentkaart, name="unemploymentkaart"),
  path('maps/italy/'             , views.italy, name="italy"),
  path('maps/oefenkaart/'        , views.oefenkaart, name="oefenkaart"),
  path('maps/plaatsen/'          , views.all_plaatsen, name="all-plaatsen"),
  path('maps/plaatsen/heatmap/'  , views.heatmap, name="heatmap"),
  path('maps/covidkaart/'        , views.covidkaart, name="covidkaart"),
  # metadata
  path('maps/models/'            , views.all_models, name="all-models"),
  # Apis
  path('api/maps/plaatsen/'          , views.PlaatsList.as_view(), name="api-all-plaatsen"),    # GET List
  path('api/maps/plaatsen/metadata/' , views.api_metadata_plaatsen, name="api-metadata-plaatsen"),
  path('api/maps/plaatsen/<int:pk>/' , views.PlaatsDetail.as_view(), name="api-plaats-detail"), # Alle C(POST) R(GET) U(PUT) D(DELETE) requests
 
  path('api/maps/metadata/'          , views.MetadataList.as_view(), name="api-all-metadata"),    # GET List
  path('api/maps/metadata/<int:pk>/' , views.MetadataDetail.as_view(), name="api-metadata-detail"), # Alle C(POST) R(GET) U(PUT) D(DELETE) requests
  # notifications
  path('notifications/plaats/'       , views.notificatie_plaats, name="notificatie-plaats"),    # endpoint voor plaats notificaties
]

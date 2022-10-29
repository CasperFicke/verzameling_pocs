# datalab/urls.py

# Django
from django.urls import path

# local
from . import views

app_name = "datalab"

urlpatterns = [
  # Datalab
  path('datalab/'  , views.index_datalab, name="index-datalab"),
  path('kadaster/' , views.index_kadaster, name="index-kadaster"),
  # Basisregistratie Kadaster
  path('datalab/brk/nnp/' , views.brk_nnp, name="brk-nnp"),
  path('datalab/brk/np/'  , views.brk_np, name="brk-np"),
  path('datalab/brk/zg/'  , views.brk_zg, name="brk-zg"),
  path('datalab/brk/oz/'  , views.brk_oz, name="brk-oz"),
  # Geoserver
  path('datalab/geoserver/workspaces/' , views.all_workspaces_geoserver, name="all-workspaces-geoserver"),
  path('datalab/geoserver/layers/'     , views.all_layers_geoserver, name="all-layers-geoserver"),
  # Ckan
  path('datalab/ckan/datasets/'        , views.all_datasets_ckan, name="all-datasets-ckan"),
  path('datalab/ckan/datasets/<str:datasetname>' , views.show_dataset_ckan, name="show-dataset-ckan"),
]


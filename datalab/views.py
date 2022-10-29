# datalab/views.py

# django
from django.shortcuts import render
from django.core.paginator import Page, Paginator

import folium
from folium import plugins

# import pandas (data-analytics)
import pandas as pd
import geopandas as gpd

import json
import requests
import os

# Datalab indexpage
def index_datalab(request):
  title = 'index datalab'
  context = {
    'title': title
  }
  return render(request, 'datalab/index_datalab.html', context)

# BRK nietnatuurlijkpersoon
def brk_nnp(request):
  title   = 'BRK nnp'
  brk_test_apikey = os.getenv('BRK_TEST_APIKEY')
  context = {
    'title' : title
  }
  if request.method == "POST":
    nnp_ = request.POST['nnp']
    url     = 'https://api.brk.kadaster.nl/esd-eto-apikey/bevragen/v1/kadasternietnatuurlijkpersonen?'
    params = {
      'q'  : nnp_
    }
    headers = {
      'X-Api-Key'   : brk_test_apikey,
      'Host'        : 'api.brk.kadaster.nl',
      'content-type': 'application/json'
    }
    api_request = requests.get(url, headers=headers, params=params)
    try:
      nnp      = []
      zg_lijst = []
      api_result = json.loads(api_request.content)
      nnp = api_result['_embedded']['kadasterNietNatuurlijkPersonen'][0]
      context['nnp'] = nnp
      for item in api_result['_embedded']['kadasterNietNatuurlijkPersonen'][0]['_links']['zakelijkGerechtigden']:
        zg_item = (
          {
            'href': item['href']
          }
        )
        zg_lijst.append(zg_item)
      context['zg_lijst'] = zg_lijst
    except Exception as e:
      api_result = "Error..."
    context['api_result'] = api_result
  return render(request, 'datalab/brk_nnp.html', context)

# BRK natuurlijkpersoon
def brk_np(request):
  title   = 'BRK np'
  brk_test_apikey = os.getenv('BRK_TEST_APIKEY')
  context = {
    'title' : title
  }
  if request.method == "POST":
    np_ = request.POST['np']
    url     = 'https://api.brk.kadaster.nl/esd-eto-apikey/bevragen/v1/kadasternatuurlijkpersonen?q=' + np_
    headers = {
      'X-Api-Key'   : brk_test_apikey,
      'Host'        : 'api.brk.kadaster.nl',
      'content-type': 'application/json'
    }
    api_request = requests.get(url, headers=headers)
    try:
      np       = []
      zg_lijst = []
      api_result = json.loads(api_request.content)
      #print(api_result)
      np = api_result['_embedded']['kadasterNatuurlijkPersonen'][0]
      #np = api_result
      context['np'] = np
      for item in api_result['_embedded']['kadasterNatuurlijkPersonen'][0]['_links']['zakelijkGerechtigden']:
        zg_item = (
          {
            'href': item['href']
          }
        )
        zg_lijst.append(zg_item)
      context['zg_lijst'] = zg_lijst
    except Exception as e:
      api_result = "Error..."
    context['api_result'] = api_result
  return render(request, 'datalab/brk_np.html', context)

# BRK zakelijkgerechtigde
def brk_zg(request):
  title   = 'BRK zg'
  brk_test_apikey = os.getenv('BRK_TEST_APIKEY')
  zg_    = request.POST['zg']
  print(zg_)
  url     = 'https://api.brk.kadaster.nl/esd-eto-apikey/bevragen/v1/kadastraalonroerendezaken/22360467970000/zakelijkgerechtigden/' + zg_
  headers = {'X-Api-Key': brk_test_apikey,
    'Host': 'api.brk.kadaster.nl',
    'content-type': 'application/json'
  }
  api_request = requests.get(url, headers=headers)
  try:
    zg = []
    api_result = json.loads(api_request.content)
    #print(api_result)
    zg = api_result
    #zg = api_result
  except Exception as e:
    api_result = "Error..."
  
  context ={
    'title' : title,
    'api_result': api_result,
    'zg'    : zg
  }
  return render(request, 'datalab/brk_zg.html', context)

# BRK onroerende zaak
def brk_oz(request):
  title   = 'BRK oz'
  brk_test_apikey = os.getenv('BRK_TEST_APIKEY')
  context = {
    'title' : title
  }
  if request.method == "POST":
    oz_    = request.POST['oz']
    url    = 'https://api.brk.kadaster.nl/esd-eto-apikey/bevragen/v1/kadastraalonroerendezaken/' + oz_
    params = {
      'q'  : oz_
    }
    headers = {'X-Api-Key': brk_test_apikey,
      'Host': 'api.brk.kadaster.nl',
      'content-type': 'application/json'
    }
    api_request = requests.get(url, headers=headers, params=params)
    try:
      oz = []
      api_result = json.loads(api_request.content)
      #print(api_result)
      oz = api_result
      context['oz'] = oz
      m = folium.Map(
        location=[52.16409, 5.96595],
        zoom_start=20
      )
      #print('begrenzing perceel = ', oz['begrenzingPerceel'])
      perceel = gpd.GeoDataFrame(oz['begrenzingPerceel'])
      #perceel = perceel.set_crs("EPSG:28992", allow_override=True)
      # convert crs to WGS84
      # perceel = perceel.to_crs("EPSG:4326")
      #print('perceel = ', perceel)

      from shapely.geometry import Polygon
      clean_geoms = pd.DataFrame([["Polygon", "[[[-96.568927, 46.769008], [-96.5689454, 46.7705433], [-96.5726564, 46.7705222], [-96.572638, 46.7689868], [-96.568927, 46.769008]]]"]],
                           columns=["field_geom_type", "geometry"])
      #print(clean_geoms)
      data = Polygon(eval(clean_geoms.geometry.iloc[0])[0])
      # add polygon
      folium.Polygon([(53.62, 8.07), (54.66, 9.09), (54.62, 7.07)],
      color = '#800080',
      weight = 4,
      fill = True,
      fill_color = '#118822',
      fill_opacity = 0.5,
      ).add_to(m)
      gdf = gpd.GeoSeries(data)
      dataType = gdf.dtype
      print('Data type of Dataframe :')
      print(dataType)
      print(gdf)

      # read file
      gdf = gpd.read_file("data/RD_bkr_perceel.json")
      # set coordinate reference system (crs) to RD
      gdf = gdf.set_crs("EPSG:28992", allow_override=True)
      # convert crs to WGS84
      gdf = gdf.to_crs("EPSG:4326")
      dataTypeDict = dict(gdf.dtypes)
      print('Data type of each column of Dataframe :')
      print(dataTypeDict)
      print(gdf)
      # add layer to map
      folium.GeoJson(
        data = gdf['geometry'],
        style_function = lambda x: {'fillcolor': 'orange'}
      ).add_to(m)

      plugins.Fullscreen().add_to(m)
      m = m._repr_html_()
      context['m'] = m
    except Exception as e:
      api_result = "Error..."
    context['api_result'] = api_result
  return render(request, 'datalab/brk_oz.html', context)

# Geoserver all workspaces
def all_workspaces_geoserver(request):
  title   = 'all workspaces'
  geoserver_test_apikey = os.getenv('GEOSERVER_TEST_APIKEY')
  url     = 'https://dpt.purmerend.nl/geoserver/rest/workspaces/'
  headers = {'Authorization': geoserver_test_apikey,
    'Host': 'dpt.purmerend.nl',
    'content-type': 'application/json'
  }
  api_request = requests.get(url, headers=headers)
  try:
    ws_lijst   = []
    api_result = json.loads(api_request.content)
    
    ws_lijst   = api_result['workspaces']['workspace']
    print(ws_lijst)
  except Exception as e:
    api_result = "Error..."
  
  context ={
    'title'      : title,
    'api_result' : api_result,
    'ws_lijst'   : ws_lijst
  }
  return render(request, 'datalab/all_workspaces_geoserver.html', context)

# Geoserver all layers
def all_layers_geoserver(request):
  title   = 'geoserverlayers'
  geoserver_test_apikey = os.getenv('GEOSERVER_TEST_APIKEY')
  url     = 'https://dpt.purmerend.nl/geoserver/rest/layers/'
  headers = {'Authorization': geoserver_test_apikey,
    'Host': 'dpt.purmerend.nl',
    'content-type': 'application/json'
  }
  api_request = requests.get(url, headers=headers)
  layer_lijst = []
  try:
    api_result  = json.loads(api_request.content)
    layer_lijst = api_result['layers']['layer']
    
  except Exception as e:
    api_result = "Error..."
  layer_count = len(layer_lijst)
  # Set up pagination
  paginator     = Paginator(layer_lijst, 50)
  page_number   = request.GET.get('page')
  layers_page   = paginator.get_page(page_number)
  page_count    = "a" * layers_page.paginator.num_pages
  is_paginated  = layers_page.has_other_pages
  context = {
    'title'       : title,
    'api_result'  : api_result,
    'layer_lijst' : layer_lijst,
    'aantal'      : layer_count,
    'page_obj'    : layers_page,
    'is_paginated': is_paginated,
    'page_count'  : page_count
  }
  return render(request, 'datalab/all_layers_geoserver.html', context)
  
# CKAN indexpage
def all_datasets_ckan(request):
  title = 'all ckan'
  ckan_prod_apikey = os.getenv('CKAN_PROD_APIKEY')
  url     = 'https://datalab.purmerend.nl/data/api/3/action/package_list'
  headers = {'Authorization': ckan_prod_apikey,
    'Host': 'datalab.purmerend.nl',
    'content-type': 'application/json'
  }
  api_request = requests.get(url, headers=headers)
  try:
    data_lijst   = []
    api_result = json.loads(api_request.content)
    data_lijst   = api_result['result']
  except Exception as e:
    api_result = "Error..."
  context ={
    'title'      : title,
    'api_result' : api_result,
    'data_lijst' : data_lijst
  }
  return render(request, 'datalab/all_datasets_ckan.html', context)

# show CKAN dataset
def show_dataset_ckan(request, datasetname):
  title = 'ckan'
  ckan_prod_apikey = os.getenv('CKAN_PROD_APIKEY')
  url     = 'https://datalab.purmerend.nl/data/api/3/action/package_show'
  payload = {'id': datasetname}
  headers = {'Authorization': ckan_prod_apikey,
    'Host': 'datalab.purmerend.nl',
    'content-type': 'application/json'
  }
  api_request = requests.get(url, data=json.dumps(payload), headers=headers)
  try:
    dataset  = []
    api_result = json.loads(api_request.content)
    dataset  = api_result['result']
  except Exception as e:
    api_result = "Error..."
  context ={
    'title'      : title,
    'api_result' : api_result,
    'dataset'    : dataset
  }
  return render(request, 'datalab/show_dataset_ckan.html', context)

# Kadaster indexpage
def index_kadaster(request):
  title = 'index kadaster'
  context = {
    'title': title
  }
  return render(request, 'datalab/index_kadaster.html', context)
# maps/views.py

# django
from cgi import test
from turtle import fillcolor
from django.db.models import fields, query
from django.http.response import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from django.core import serializers

import json
import datetime
import os

import folium
from folium import plugins

# drf
from rest_framework import generics, permissions
from rest_framework.serializers import Serializer
from .serializers import MetadataSerializer, PlaatsSerializer

# import pandas (data-analytics)
import pandas as pd
import geopandas as gpd
from branca.element import Template, MacroElement
# from pandas.io.formats.format import Datetime64TZFormatter

# local
from .models import Land, Metadata, Plaats, Unemploymentrate
from dental.mixins import Directions

# Allmodels
def all_models(request):
  title = 'all models'
  modellist = ContentType.objects.all()
  context = {
    'title'     : title,
    'modellist' : modellist
  }
  return render(request, 'maps/all_models.html', context)

# Basic view for google kaart
def google_basis(request):
  title = 'google-basis'
  context = {
    'title'         :title,
	  'google_api_key': os.getenv('GOOGLE_API_KEY'),
	  'base_country'  : 'NL'}
  return render(request, 'maps/google_basis.html', context)

# Insert route to display in google map
def google_route(request):
  title = 'google-route'
  context = {
    'title'         : title,
	  'google_api_key': os.getenv('GOOGLE_API_KEY'),
	  'base_country'  : 'NL'}
  return render(request, 'maps/google_route.html', context)

# Display google map and directions
def google_map(request):
  title = 'google-map'
  # startpunt
  lat_a  = request.GET.get("lat_a", None)
  long_a = request.GET.get("long_a", None)
  # eindpunt
  lat_b  = request.GET.get("lat_b", None)
  long_b = request.GET.get("long_b", None)
  # tussenpunt 1
  lat_c  = request.GET.get("lat_c", None)
  long_c = request.GET.get("long_c", None)
  # tussenpunt 2
  lat_d  = request.GET.get("lat_d", None)
  long_d = request.GET.get("long_d", None)

	# only call API if all 4 addresses are added
  if lat_a and lat_b and lat_c and lat_d:
    directions = Directions(
			lat_a  = lat_a,
			long_a = long_a,
			lat_b  = lat_b,
			long_b = long_b,
			lat_c  = lat_c,
			long_c = long_c,
			lat_d  = lat_d,
			long_d = long_d
			)
  else:
    return redirect(reverse('maps:googleroute'))

  context = {
    'title'  : title,
    'google_api_key': os.getenv('GOOGLE_API_KEY'),
    'base_country': 'NL',
    'lat_a' : lat_a,
    'long_a': long_a,
    'lat_b' : lat_b,
    'long_b': long_b,
    'lat_c' : lat_c,
    'long_c': long_c,
    'lat_d' : lat_d,
    'long_d': long_d,
    'origin'      : f'{lat_a}, {long_a}',
    'destination' : f'{lat_b}, {long_b}',
    'directions'  : directions,
	}
  return render(request, 'maps/google_map.html', context)

# folium oefenkaart
def oefenkaart(request):
  title = 'oefenkaart'
  context = {
    'title' : title,
  }
  tooltip = 'Click voor meer info'
  map = folium.Map(
    location   = [52.6, 5.0],
    tiles      = 'openstreetmap',
    zoom_start = 5
  )
  folium.TileLayer('openstreetmap').add_to(map)
  folium.TileLayer('Stamen Terrain', attr='stamen').add_to(map)
  folium.TileLayer('Stamen Toner').add_to(map)
  folium.TileLayer('Stamen Watercolor').add_to(map)
  folium.TileLayer('CartoDB Positron').add_to(map)
  folium.TileLayer('CartoDB Dark_matter').add_to(map)
  folium.TileLayer('https://service.pdok.nl/hwh/luchtfotorgb/wmts/v1_0/Actueel_ortho25/EPSG:3857/{z}/{x}/{y}.jpeg',
    name='nlmaps luchtfoto',
    attr='nlmaps luchtfoto'
  ).add_to(map)
  folium.TileLayer('https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/standaard/EPSG:3857/{z}/{x}/{y}.png',
    name='nlmaps standaard',
    attr='nlmaps standaard'
  ).add_to(map)
  # add layer for landen markers
  landenMarkersLayer = folium.FeatureGroup(name="Landen markers").add_to(map)
  # add layer for test shapes
  testShapesLayer = folium.FeatureGroup(name="test shapes").add_to(map)
  folium.LayerControl().add_to(map)
  
  # Add landen uit de db
  landen            = Land.objects.all()
  context['landen'] = landen
  df = pd.DataFrame(list(landen.values()))
  # print(df.nlargest(3,['aant_inwoners']))
  # print(df)
  # print(df.info())
  for (index, rows) in df.iterrows():
    lat = rows.loc['latitude']
    lng = rows.loc['longitude']
    aant_inw = rows.loc['aant_inwoners']
    popup = str(rows.loc['naam'] + ' ' + str(rows.loc['aant_inwoners'])).title()
    if aant_inw > 250:
      mc = 'green'
      mi = 'leaf'
    else:
      mc = 'red'
      mi = 'bolt'
    folium.Marker(
      location=[lat, lng],
      popup=popup,
      tooltip=tooltip,
      icon = folium.Icon(color=mc, prefix='fa', icon=mi)
    ).add_to(landenMarkersLayer)
  # marker
  folium.Marker([53.5, 6.05],
    popup='<strong>Naam van lokatie 2</strong>',
    tooltip=tooltip,
    icon=folium.Icon(icon='cloud', color='green')
  ).add_to(testShapesLayer)
  # text
  folium.Marker([52.5, 6.5],
    popup=folium.Popup('<i>Naam van lokatie 3</i>'),
    tooltip=tooltip,
    icon=folium.DivIcon(html="""Tekst op de kaart <b>Vet</b>""", class_name='mapText'),
  ).add_to(map)
  
  # get map variable name
  mapJsVar = map.get_name()
  # styling for the text (inject html in to the map layer)
  map.get_root().html.add_child(folium.Element("""
    <style>
      .mapText {
        color: blue;
        font-size: large;
        white-space: nowrap
      }
    </style>
    <script type="text/javascript">
      window.onload = function(){
        var sizeFromZoom = function(z){return (0.5*z)+"em"}
        var updateTextSizes = function(){
          var mapZoom = {map}.getZoom();
          var txtSize = sizeFromZoom(mapZoom);
          $(".mapText").css("font-size", txtSize);
        }
      updateTextSizes();
      {map}.on("zoomend", updateTextSizes);
      }
    </script>
  """.replace("{map}", mapJsVar)))

  # Circle marker
  folium.CircleMarker(
    location=[53.5, 6.05],
    radius=40,
    popup='Hier ongeveer',
    tooltip=tooltip,
    color='#428bca',
    fill=True,
    fill_color='#428bca'
  ).add_to(testShapesLayer)
  # add scaling circle
  folium.Circle(location=[53.5, 6.05],
    radius=50000,
    color='purple',
  ).add_to(testShapesLayer)
  # add scaling rectangle
  folium.Rectangle([(52.62, 5.07), (54.66, 6.09)],
  fill = True,
  fill_color = '#FF00FF',
  fill_opacity = 0.2,
  ).add_to(testShapesLayer)
  # add polyline
  folium.PolyLine([(50.62, 5.07), (51.66, 6.09), (51.62, 4.07), (55.16, 2.59)],
  color = '#080080',
  weight = 4,
  ).add_to(testShapesLayer)
  # add polygon
  folium.Polygon([(53.62, 8.07), (54.66, 9.09), (54.62, 7.07)],
  color = '#800080',
  weight = 4,
  fill = True,
  fill_color = '#118822',
  fill_opacity = 0.5,
  ).add_to(testShapesLayer)
  
  # inject html into the map html
  map.get_root().html.add_child(folium.Element("""
    <div style="position: fixed; 
      top: 50px; left: 70px; width: 150px; height: 70px; 
      background-color:orange; border:2px solid grey;z-index: 900;">
      <h5>Hello World!!!</h5>
      <button>Test Button</button>
    </div>
  """))
    
  # add fullscreen button to the map
  plugins.Fullscreen().add_to(map)
  # render map as html
  map = map._repr_html_()
  context['map'] = map
  return render(request, 'maps/oefenkaart.html', context)

# folium Heatmap
def heatmap(request):
  title    = 'heatmap'
  plaatsen = Plaats.objects.all()
  large_cities = [plaats for plaats in plaatsen if plaats.aant_inwoners > 200]
  # map basis
  map = folium.Map(
    location   = [52.6, 5.0],
    tiles      = 'CartoDB Dark_matter',
    zoom_start = 5
  )
  # add openstreetmap layer
  folium.TileLayer('openstreetmap').add_to(map)
  # add layer for heatmap
  heatmapLayer = folium.FeatureGroup(name="heatmap").add_to(map)
  # add layer for info markers
  infoLayer = folium.FeatureGroup(name="info markers").add_to(map)
  # create infomarkers layer
  plaatsen_list = Plaats.objects.values_list('latitude', 'longitude', 'aant_inwoners')
  df = pd.DataFrame(list(plaatsen.values()))
  for (index, rows) in df.iterrows():
    lat = rows.loc['latitude']
    lng = rows.loc['longitude']
    aant_inw = rows.loc['aant_inwoners']
    popup = str(rows.loc['naam'] + ' ' + str(rows.loc['aant_inwoners'])).title()
    folium.Marker(
      location=[lat, lng],
      tooltip = 'click for info',
      popup=popup,
      icon = folium.Icon(color='blue')
    ).add_to(infoLayer)
  # add fullscreen button
  plugins.Fullscreen(position='topright').add_to(map)
  plugins.HeatMap(plaatsen_list).add_to(heatmapLayer)
  # add layercontrol
  folium.LayerControl().add_to(map)
  map = map._repr_html_()
  context = {
    'title'    : title,
    'plaatsen' : plaatsen,
    'large_cities': large_cities,
    'map'      : map
  }
  return render(request, 'maps/heatmap.html', context)

# mapbox map; default_map 
def default_map(request):
  title = 'Mapbox kaart'
  mapbox_access_token = 'pk.eyJ1IjoiY2ZpY2tlIiwiYSI6ImNrbGIwYzg0ajBxa2EydnM4eXR1ZHp0dGgifQ.x9EoFA_ddcBU5HkBDGZ-eA'
  context = {
    'title': title,
    'mapbox_access_token': mapbox_access_token
  }
  return render(request, 'maps/default_map.html', context)

# folium basiskaart
def basiskaart (request):
  title = 'Folium basiskaart'
  m = folium.Map(location=[43.062776, -75.420884], tiles="cartodbpositron", zoom_start=7)
  #gdf = gpd.read_file("data/Newyork/Counties_Shoreline.shp")
  #gdf = gdf.to_crs("EPSG:4326")
  #print(gdf.crs)
  #print(gdf)
  #folium.GeoJson(data=gdf["geometry"]).add_to(m)
  #folium.GeoJson(data=gdf["geometry"][6]).add_to(m)

  m = m._repr_html_()
  context = {
    'title': title,
    'm': m,
  }
  return render(request, 'maps/basiskaart.html', context)

# openlayerskaart
def openlayerskaart (request):
  title = 'Openlayerskaart'
  context = {
    'title': title,
  }
  return render(request, 'maps/openlayerskaart.html', context)

# folium unemploymentkaart
def unemploymentkaart (request):
  title = 'unemploymentkaart'
  # load rates from db
  rate = Unemploymentrate.objects.all()
  # convert object to dataframe
  df   = pd.DataFrame(list(rate.values('state', 'percentage')))
  # convert datatype in dataframe
  convert_dict = {
    'percentage': float
  }
  # doe iets met het dataframe
  df = df.astype(convert_dict)
  # set location state-geometryfile
  us_states = os.path.join('data', 'us-states.json')
  # unemployment_data = os.path.join('data', 'us_unemployment.csv')
  # state_data        = pd.read_csv(unemployment_data)
  # read the file and print it.
  # geoJSON_df = gpd.read_file(us_states)
  # print(geoJSON_df.head())

  # Basiskaart
  m = folium.Map(
    location   = [48, -102],
    zoom_start = 4,
    tiles='Stamen Terrain'
  )
  # add 
  featuregroup1=folium.FeatureGroup(name='Popup', show=True)
  m.add_child(featuregroup1)
  # add openstreetmap layer
  folium.TileLayer('openstreetmap').add_to(m)
  # add choropleth layer
  folium.Choropleth(
    geo_data       = us_states,
    name           = 'unemployment rate',
    data           = df,
    columns        = ['state', 'percentage'],
    key_on         = 'feature.id',
    fill_color     = 'YlOrRd',
    fill_opacity   = 0.8,
    line_opacity   = 0.2,
    legend_name    = 'Unemployment Rate %',
    reset          = True,
    highlight      = True,
    nan_fill_color = 'White',
  ).add_to(m)

  # Add hover functionality
  style_function = lambda x: {
    'fillColor': '#ffffff',
    'color'    : '#000000',
    'weight'   : '0.1'
  }
  highlight_function = lambda x: {
    'fillColor'  : '#000000',
    'fillOpacity': 0.50,
    'weight'     : '0.1'
  }
  NIL = folium.features.GeoJson(
    data = us_states,
    style_function     = style_function,
    highlight_function = highlight_function,
    tooltip   = folium.features.GeoJsonTooltip(
      fields  = ['name', 'density'],
      aliases = ['name', 'density'],
      style   = ("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px")
    )
  )
  featuregroup1.add_child(NIL)
  m.keep_in_front(featuregroup1)
  
  # Add dark and light mode. 
  folium.TileLayer('cartodbdark_matter',name="dark mode",control=True).add_to(m)
  folium.TileLayer('cartodbpositron'   ,name="light mode",control=True).add_to(m)

  # layer controller. 
  folium.LayerControl(collapsed=False).add_to(m)
  # Save map
  # m.save('maps/templates/maps/unemploymentkaart.html')
  m = m._repr_html_()
  context = {
    'title': title,
    'm'    : m
  }
  return render(request, 'maps/unemploymentkaart.html', context)

# zwemkaart
def zwemkaart(request):
  title   = 'kaarten'
  tooltip = 'Click voor meer info'
  # zwemgebied
  zwemgebied = os.path.join('data', 'zwemzone.json')
  # create map
  m = folium.Map(
    location=[52.62, 5.07],
    zoom_start=11.5
  )
  folium.TileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png',
    name='openseamap',
    attr='openseamap'
  ).add_to(m)
  # voeg zwemgebied toe aan de kaart
  folium.GeoJson(
    zwemgebied,
    name    = 'zwem',
    popup   = 'Zwemgebied',
    tooltip = tooltip,
    style_function=lambda feature: {
      'fillColor': '#428bca',
      'color': 'black',
      'weight': 2,
      'dashArray': '5, 5'
    }
  ).add_to(m)
  folium.LayerControl().add_to(m)
  m = m._repr_html_()
  context = {
    'title': title,
    'm': m,
  }
  return render(request, 'maps/zwemkaart.html', context)

# folium italy kaart
def italy (request):
  title = 'italie'
  # Basiskaart
  m = folium.Map(
    location   = [40, 15],
    zoom_start = 5,
  )
  
  def style_function(feature):
    area = int(feature['properties']['area'])
    return {
      'fillOpacity': 0.5,
      'weight'     : 0.5,
      'fillColor'  : 'green'
        if area < 10008018378 \
        else 'orange'
          if area< 20008018378\
          else 'red'
      }

  gjson = folium.GeoJson("https://raw.githubusercontent.com/stefanocudini/leaflet-geojson-selector/master/examples/italy-regions.json",
    style_function=style_function
  ).add_to(m)

  template = """
    {% macro html(this, kwargs) %}
      <!doctype html>
        <head>
          <title>jQuery UI Draggable - Default functionality</title>
          <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
          <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
          <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
          <script>
            $( function() {
              $( "#maplegend" ).draggable({
                  start: function (event, ui) {
                    $(this).css({
                      right: "auto",
                      top: "auto",
                      bottom: "auto"
                    });
                  }
              });
            });
          </script>
        </head>
        <body>
          <div id='maplegend' class='maplegend' 
            style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
            border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'> 
          <div class='legend-title'>Legenda</div>
            <div class='legend-scale'>
              <ul class='legend-labels'>
                <li><span style='background:red;opacity:0.7;'></span>Big</li>
                <li><span style='background:orange;opacity:0.7;'></span>Medium</li>
                <li><span style='background:green;opacity:0.7;'></span>Small</li>
              </ul>
            </div>
          </div>
        </body>
      </html>
      <style type='text/css'>
        .maplegend .legend-title {
          text-align: left;
          margin-bottom: 5px;
          font-weight: bold;
          font-size: 90%;
          }
        .maplegend .legend-scale ul {
          margin: 0;
          margin-bottom: 5px;
          padding: 0;
          float: left;
          list-style: none;
          }
        .maplegend .legend-scale ul li {
          font-size: 80%;
          list-style: none;
          margin-left: 0;
          line-height: 18px;
          margin-bottom: 2px;
          }
        .maplegend ul.legend-labels li span {
          display: block;
          float: left;
          height: 16px;
          width: 30px;
          margin-right: 5px;
          margin-left: 0;
          border: 1px solid #999;
          }
        .maplegend .legend-source {
          font-size: 80%;
          color: #777;
          clear: both;
          }
        .maplegend a {
          color: #777;
          }
      </style>
    {% endmacro %}
  """
  macro = MacroElement()
  macro._template = Template(template)

  m.get_root().add_child(macro)

  m = m._repr_html_()
  context = {
    'title': title,
    'm'    : m
  }
  return render(request, 'maps/italy.html', context)

# FOLIUM COVIDKAART
def covidkaart(request):
  latitude = 52.1500
  longitude = 5.7970
  current_url='https://opendata.arcgis.com/datasets/620c2ab925f64ed5979d251ba7753b7f_0.geojson' 
  current_data = gpd.read_file(current_url)

  # building a base map
  Map = folium.Map(
    location = [latitude, longitude],
    zoom_start = 7)

  # adding a choropleth map
  bins=[0, 100, 250, 500, 750, 1000]
  folium.Choropleth(
      geo_data=current_url,
      name='choropleth',
      data=current_data,
      columns=['Municipality', 'Reported_100000'],
      key_on='feature.properties.Gemeentenaam',
      fill_color='YlOrRd',
      fill_opacity=0.6,
      line_opacity=0.2,
      legend_name='Reported cases per 100000',
      bins=bins,
      reset=True
  ).add_to(Map)

  Map.save('Reported_NL.html')

  return render(request, 'covidkaart.html')

# all-plaatsen
def all_plaatsen(request):
  title    = 'alle plaatsen'
  plaatsen = Plaats.objects.all()
  metadata = Metadata.objects.filter(id=2)
  context = {
    'title'    : title,
    'plaatsen' : plaatsen,
    'metadata' : metadata
  }
  return render(request, 'maps/all_plaatsen.html', context)

# Metadata plaatsen
def api_metadata_plaatsen(request):
  obj    = Metadata.objects.get(id = '2')
  data   = serializers.serialize('json', [obj,])
  struct = json.loads(data)
  data   = json.dumps(struct[0])
  #return HttpResponse(data, mimetype='application/json') 
  return HttpResponse(data)

# Notificatie plaats
def notificatie_plaats(request):
  if request.method == "POST":
    data = request.POST
    messages.success(request, ("plaats has been added!"))
    return HttpResponse('plaats actie ontvangen')
  else:
    return HttpResponse('niets...')

# Api views
# List all plaatsen
class PlaatsList(generics.ListCreateAPIView):
  queryset           = Plaats.objects.all()
  #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  serializer_class   = PlaatsSerializer

# ReadUpdateDelete plaats
class PlaatsDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset           = Plaats.objects.all()
  #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  serializer_class   = PlaatsSerializer

# List all metadata
class MetadataList(generics.ListCreateAPIView):
  queryset           = Metadata.objects.all()
  #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  serializer_class   = MetadataSerializer

# ReadUpdateDelete Metadata
class MetadataDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset           = Metadata.objects.all()
  #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  serializer_class   = MetadataSerializer
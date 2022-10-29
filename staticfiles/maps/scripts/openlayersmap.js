/* maps/static/maps/styles/openlayersmap.js*/

window.onload = init;

function init(){
  // Declare a Tile layer with OSM source
  var osmLayer = new ol.layer.Tile({
    source: new ol.source.OSM()
  });
  // Declare a Tile layer with Stamen terrrain source
  var st_terrain = new ol.layer.Tile({
    source: new ol.source.Stamen({layer: 'terrain'})
  });
  // Declare a Tile layer with Stamen-terrain labels source
  var st_labels = new ol.layer.Tile({
    source: new ol.source.Stamen({layer: 'terrain-labels'})
  });
  // center, transforming to map projection
  var center = ol.proj.transform([5.4, 51.8], 'EPSG:4326', 'EPSG:3857');

  // overlay for position of the center
  var overlay_c = new ol.Overlay({
    position : center,
    element  : document.getElementById('overlay_c')
  });
  // overlay for location
  var overlay_loc = new ol.Overlay({
    element: document.getElementById('overlay_loc'),
    positioning: 'bottom-center'
  });
  // Create a View, set it center and zoom level
  var myview = new ol.View({
    center: center,
    zoom: 6
  });

  // Instanciate a Map, set the object target to the map DOM id
  var map = new ol.Map({
    target: 'map',
  });
  // Set the view for the map
  map.setView(myview);
  // Add the osm layer to the Map
  map.addLayer(osmLayer);
  // Add the stamwen labels layer to the Map
  map.addLayer(st_labels);
  // Add center  overlay to the map
  map.addOverlay(overlay_c);
 
  // register an event handler for the click event
  map.on('click', function(event) {
    // extract the spatial coordinate of the click event in map projection units
    var coord = event.coordinate;
    // transform it to decimal degrees
    var degrees = ol.proj.transform(coord, 'EPSG:3857', 'EPSG:4326');
    // format a human readable version
    var hdms = ol.coordinate.toStringHDMS(degrees);
    // update the overlay element's content
    var element = overlay_loc.getElement();
    element.innerHTML = hdms;
    // position the element (using the coordinate in the map's projection)
    overlay_loc.setPosition(coord);
    // and add it to the map
    map.addOverlay(overlay_loc);
  });
  
  // Layer Styles
  const fillStyle = new ol.style.Fill({
    color: [255, 0, 0, 255]
  });
  // create a vector source that loads a GeoJSON file
  var vectorSource = new ol.source.Vector({
    projection: 'EPSG:3857',
    url: 'https://c.data.osmbuildings.org/0.2/anonymous/tile/15/17607/10743.json',
    format: new ol.format.GeoJSON(),
  });
  // a vector layer to render the source
  var vectorLayer = new ol.layer.Vector({
    source: vectorSource
  });
  map.addLayer(vectorLayer);
}


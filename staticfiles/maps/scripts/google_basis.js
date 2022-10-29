/* maps/static/maps/styles/google_basis.js*/

function initMap() {
  map = new google.maps.Map(document.getElementById("map-route"), {
    center: { lat: 52.5, lng: 5.15 },
    zoom: 10,
  });
}

var theMap;
var clusterOptions = {gridSize: 50, maxZoom: 18};;
var cluster = false;

var markersArray = [];

var map_options = {
	zoom: 16,
	center: new google.maps.LatLng(41.8562461, 12.4688934),
	mapTypeId: google.maps.MapTypeId.ROADMAP
};

function add_point(title, lat, lon, fullData) {
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(lat,lon), 
		map: null,
		title:title
	});
	markersArray.push( marker );

	google.maps.event.addListener(marker, 'click', function() {
		theMap.setCenter(marker.getPosition());
		theMap.setZoom(18);
		window.location = '/'+point['id'];
	});
	
	return marker;
}

function clearMarkers() {
	if (markersArray) {
		for (i in markersArray) {
			markersArray[i].setMap(null);
			delete markersArray[i];
		}
	}
	markersArray = [];
}

function ajaxLoadAllMarkers(){
	clearMarkers();
	$.getJSON('/api/points', function(data) {
		$.each(data, function(num, point) {
			add_point(point['title'], point['lat'], point['lon'], point);
		});
	}).complete(function() { 
        if(cluster == false) {
        	cluster = new MarkerClusterer(theMap, markersArray, clusterOptions);
        }
	});
}


$(function(){
    theMap = new google.maps.Map(document.getElementById('map_canvas'), map_options);
    //google.maps.event.addDomListener(window, 'load', function(){ajaxLoadAllMarkers();});
    
    google.maps.event.addListener(theMap, 'idle', function() {
    	ajaxLoadAllMarkers();
    });
});
var theMap;
var clusterOptions = {};;
var cluster;

var markersArray = [];

var mapOptions = {
      center: new google.maps.LatLng(41.8562461, 12.4688934),
      zoom: 14,
      mapTypeId: google.maps.MapTypeId.ROADMAP
};

function add_point(point) {
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(point['coordinates']['lat'],point['coordinates']['lng']), 
		map: null,
		title:point['title']
	});
	markersArray.push( marker );

	google.maps.event.addListener(marker, 'click', function() {
		theMap.setCenter(marker.getPosition());
		theMap.setZoom(18);
		window.location = '/p/'+point['id'];
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
			add_point(point);
		});
		cluster = new MarkerClusterer(theMap, markersArray, clusterOptions);
	});
}

//google.maps.event.addDomListener(window, 'load', function(){ajaxLoadAllMarkers();});


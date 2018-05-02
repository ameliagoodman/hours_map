

var geocoder = new google.maps.Geocoder(); 
var center = {lat: 29.4745861, lng: -24.4835251};
map = new google.maps.Map(document.getElementById('map'), {
  center: center,
  zoom: 3
});

angular.module('nodeMap', [])
.controller('mainController', ($scope, $http) => {
  $scope.mapData = {};
  // Get all todos
  $http.get('/api/v1/maps')
  .success((data) => {
    $scope.mapData = data;
    for (var i = 0; i < data.length; i++) {
    	console.log(data[i]['location'])
	    var latlng = new google.maps.LatLng(parseFloat(data[i]['lat']),parseFloat(data[i]['long']));
	    var marker = new google.maps.Marker({
			position: latlng,
			address_name: data[i]['location'],
			link: data[i]['link'],
			map: map,
			clickableIcons: true
		});
		marker.addListener('click', function() {
		    $('#location').text(this.address_name);
		    $('#link').attr("href", this.link);
		    $('#link').text(this.link);
		    map.panTo(this.getPosition());
		    console.log(this.address_name);
		});
    }
  })
  .error((error) => {
    console.log('Error: ' + error);
  });
});

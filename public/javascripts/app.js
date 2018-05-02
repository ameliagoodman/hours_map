

var geocoder = new google.maps.Geocoder(); 
var center = {lat: 29.4745861, lng: -24.4835251};
map = new google.maps.Map(document.getElementById('map'), {
  center: center,
  zoom: 3
});

angular.module('nodeMap', [])
.controller('mainController', ($scope, $http) => {
  $scope.mapData = {};
  $scope.location = {'name': "Click a marker to get started",
					 'link': ""
					 };
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
			$scope.location = {'name': this.address_name,
		    				   'link': this.link
		    				  }
		    $scope.$apply();
		    map.panTo(this.getPosition());
		});
    }
  })
  .error((error) => {
    console.log('Error: ' + error);
  });
});

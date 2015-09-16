// map controller for sbcatalog frontend
app.controller("MapController", function($http, $rootScope) {

    // create the map (map container must be loaded in dom)
    var map = L.map('map').setView([41.89, 12.53], 6);

    // return index of a marker in markers that match coordinates
    var getMarkerFromCoords = function(coords, markers) {
        return _.findIndex(markers, function(x) {
            return _.isEqual(x, coords);
        });
    };

    // add open street map layer to map
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">' +
                     'OpenStreetMap</a> contributors'
    }).addTo(map);

    // get the supplier data and add to the map
    $http.get($rootScope.geoApiBaseUrl + '/geo/supplier/').success(function(data) {
        suppliers = data._items;
        markers = [];

        suppliers.forEach(function(s) {
            c = s.coords.reverse();

            // this will move the point of a
            // random offset if there is duplicate
            while(getMarkerFromCoords(c, markers) >= 0) {
                r = Math.random;
                c[0] += (r() - r()) / 1000.0;
                c[1] += (r() - r()) / 1000.0;
            }

            // push into the markers array
            markers.push(c);

            // add to map
            L.marker(c).addTo(map)
                .bindPopup("<b>" + s.name + "</b><br>" + s.address + "<br>" +
                           (s.webSite? '<a href="' + s.webSite + '">' +
                            s.webSite + '</a>': ''));
        });
    });
});

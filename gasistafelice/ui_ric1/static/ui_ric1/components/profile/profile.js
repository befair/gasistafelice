app.controller("ProfileController", function ($http, $rootScope, ngDialog, parsingNumbers) {

    // create the map (map container must be loaded in dom)
    var map = L.map('map').setView([41.89, 12.53], 10);
    
    // add open street map layer to map
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">' +
                     'OpenStreetMap</a> contributors'
    }).addTo(map);

    this.person = $rootScope.person;

    this.clickToOpen = function () {
        ngDialog.open({ 
            template: 'popupTemplate',
            className: 'ngdialog-theme-flat',
            scope: $rootScope
        });
    };

    var coords;

    angular.forEach(this.person.gas_list, function(gas) {
        hq = gas.headquarter;

        // add to map
        L.marker([hq.lat, hq.lon]).addTo(map)
            .bindPopup("<b>" + gas.name + "</b><br>" + hq.address + " " + hq.city); 

        // remember coords to center the map
        coords = new L.LatLng(hq.lat, hq.lon);
    });

    // center the map to last marker
    map.panTo(coords);

}); 

/* TODO DISASTER RECOVERY...
 *
        var id = $routeParams.id;
        $scope.path_gmid=$.absurl_api+"gasmember/"+$rootScope.gasmemberID+"/?format=json";
        $http.get($.absurl_api+'gasmember/'+$rootScope.gasmemberID+'/?format=json').success(function(data){
          $scope.balance = parsingNumbers.parsing(data.balance,2);  
          $scope.tb = parsingNumbers.parsing(data.total_basket);
          $scope.tbtbd = parsingNumbers.parsing(data.total_basket_to_be_delivered);
          var appo = $scope.tb + $scope.tbtbd;
          $scope.resume = $scope.balance - appo;
          $scope.resume = parsingNumbers.parsing($scope.resume,2);
        });
        
        $http.get($.absurl_api+'person/'+$routeParams.pe+'/?format=json').success(function(data){
            
              $.each(data.gas_list, function(index, element){
                $.each(data.gasmembers, function(index2,element2){
                 $http.get($.absurl_api+'gasmember/'+element2+'/?format=json').success(function(data){ 
                        $scope.tb = parsingNumbers.parsing(data.total_basket);
                        $scope.tbtbd = parsingNumbers.parsing(data.total_basket_to_be_delivered);
                        $scope.balance = parsingNumbers.parsing(data.balance);
                    });
                 });
              });            
            
            $scope.scheda = data;
            $.each(data.contact_set, function(index, element){
                $scope.contact = element;
                if (element.flavour == "EMAIL")
                {
                    $scope.email = element;
                }
                else
                {
                    $scope.phone = element;
                }     
            });
        });
*/

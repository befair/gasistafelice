GasistaFelice.controller('schedaController',function ($scope, $routeParams, $modal, $log, $http, ngDialog, $rootScope) {
        var id = $routeParams.id;
        // --- URL finale --- 
        //var url = 'http://localhost:8000/gasistafelice/api/v1/person/id/?format=json';
        //URL di prova    
        var url = './lib/Person'+id+'.json';
        var url2 = './lib/GASMember573Dominique.json';
        
        
        console.log("RootScope Params " + $rootScope.gasMember);    
        $scope.clickToOpen = function () {
            ngDialog.open({ template: 'popupTemplate',
                            className: 'ngdialog-theme-flat',
                            scope: $scope});
        };
       
        $http.get('./lib/GASMember573Dominique.json').success(function(data){
            $scope.tb = data.total_basket;
            $scope.tbtbd = data.total_basket_to_be_delivered;
            $scope.balance = data.balance;
        });
    
        $http.get(url2).success(function(charge_data){
            $scope.gasmember = charge_data;
        });
    
        $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
            
              $.each(data.gas_list, function(index, element){
                $.each(data.gasmembers, function(index2,element2){
                 $http.get('/gasistafelice/api/v1/gasmember/'+element2+'/?format=json').success(function(data){ 
                     $scope.tb = data.total_basket;
                        $scope.tbtbd = data.total_basket_to_be_delivered;
                        $scope.balance = data.balance;
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
});



  

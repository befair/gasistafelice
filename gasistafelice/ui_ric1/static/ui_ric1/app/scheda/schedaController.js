function schedaController($scope, $routeParams, $modal, $log, $http, ngDialog, $rootScope, parsingNumbers, r_gasmemberID) {
        var id = $routeParams.id;
        $scope.path_gmid="/gasistafelice/api/v1/gasmember/"+$rootScope.gasmemberID+"/?format=json";
        $http.get('/gasistafelice/api/v1/gasmember/'+$rootScope.gasmemberID+'/?format=json').success(function(data){
          $scope.balance = parsingNumbers.parsing(data.balance,2);  
          $scope.tb = parsingNumbers.parsing(data.total_basket);
          $scope.tbtbd = parsingNumbers.parsing(data.total_basket_to_be_delivered);
          var appo = $scope.tb + $scope.tbtbd;
          $scope.resume = $scope.balance - appo;
          $scope.resume = parsingNumbers.parsing($scope.resume,2);
        });
        
        $scope.clickToOpen = function () {
            ngDialog.open({ template: 'popupTemplate',
                            className: 'ngdialog-theme-flat',
                            scope: $scope});
        };
    
        $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
            
              $.each(data.gas_list, function(index, element){
                $.each(data.gasmembers, function(index2,element2){
                 $http.get('/gasistafelice/api/v1/gasmember/'+element2+'/?format=json').success(function(data){ 
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
}


  
schedaController.resolve = {
    r_gasmemberID : function($q, $http, $routeParams, $route, $rootScope) {
        var deferred = $q.defer();
        var appoggio = $route.current.params.pe;
        console.log(appoggio);
         $http.get('/gasistafelice/api/v1/person/'+appoggio+'/?format=json')
            .success(function(data) {
                $rootScope.gasID = data.gas_list[0].id;
                $rootScope.gasmemberID = data.gasmembers[0];
                deferred.resolve(data)
            })
            .error(function(data){
                deferred.resolve("error value");
            });

        return deferred.promise;
    }
};
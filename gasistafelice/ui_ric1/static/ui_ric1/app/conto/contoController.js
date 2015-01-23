/*angular.module('ngGasistaFelice').controller('contoController', function($scope, contoID) {
          $(function() {
            $( '#datepicker' ).datepicker();
          });
});*/

function contoController($scope, $rootScope, $routeParams, $http, contoID) {
          $(function() {
            $( '#datepicker' ).datepicker();
          });
}

function formController($scope,$http,$rootScope, $sce, parsingNumbers){
    $scope.causale = "";
    $scope.target = "";
    $scope.somma = "";
    $scope.data_causale = "";
    console.log($rootScope.gasmemberID);
    $scope.path="/gasistafelice/rest/gasmember/"+$rootScope.gasmemberID+"/balance_gm/INCOME";
    $scope.path_gmid="/gasistafelice/api/v1/gasmember/"+$rootScope.gasmemberID+"/?format=json";
    $http.get($scope.path_gmid).success(function(data){
        //$scope.balance = parseFloat(Math.round(data.balance * 100) / 100).toFixed(2);
        $scope.balance = parsingNumbers.parsing(data.balance);
    });
    
    /*
    name="INCOME" value="Esegui transazione"
    name = "target" value="" -> checkbox
    
    */
    
        $scope.transaction = function(){
            console.log($scope.data_causale);
            $http.post($scope.path, {INCOME: "Esegui transazione",
                                     amount: $scope.somma,
                                     causal: $scope.causale,
                                     date: $scope.data_causale,
                                     target: $scope.target})
            .success(function(){
                alert("Transazione effettuata!");
            })
            .error(function(){
                alert("Transazione NON effettuata, si prega di riprovare")
            });
    }
}

contoController.resolve = {
    contoID : function($q, $http, $routeParams, $route, $rootScope) {
        var deferred = $q.defer();
        var appoggio = $route.current.params.pe;
         $http.get('/gasistafelice/api/v1/person/'+appoggio+'/?format=json')
            .success(function(data) {
                $rootScope.gasmemberID = data.gasmembers[0];
                deferred.resolve(data)
            })
            .error(function(data){
                deferred.resolve("error value");
            });

        return deferred.promise;
    }
};

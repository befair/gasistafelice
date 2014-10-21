var GasistaFelice = angular.module('ngGasistaFelice', [
    'ui.bootstrap',
    'ngRoute',
    'ngDialog'
]).run(function($rootScope, $routeParams) {
    $rootScope.gasID = "10"; //default value
    $rootScope.first = true;
    $rootScope.gasmemberID = "573";
    $rootScope.personID = $routeParams.pe;
});



GasistaFelice.factory(
            "transformRequestAsFormPost",
            function() {
 
                // I prepare the request data for the form post.
                function transformRequest( data, getHeaders ) {
                    var headers = getHeaders();
                    headers[ "Content-type" ] = "application/x-www-form-urlencoded; charset=utf-8";
                    return( serializeData( data ) );
                }
                // Return the factory value.
                return( transformRequest );
 
 
                // ---
                // PRVIATE METHODS.
                // ---
                // I serialize the given Object into a key-value pair string. This
                // method expects an object and will default to the toString() method.
                // --
                // NOTE: This is an atered version of the jQuery.param() method which
                // will serialize a data collection for Form posting.
                // --
                // https://github.com/jquery/jquery/blob/master/src/serialize.js#L45
                
                function serializeData( data ) {
                    // If this is not an object, defer to native stringification.
                    if ( ! angular.isObject( data ) ) {
                        return( ( data == null ) ? "" : data.toString() );
                    }
 
                    var buffer = [];
                    // Serialize each key in the object.
                    for ( var name in data ) {
                        if ( ! data.hasOwnProperty( name ) ) {
                            continue;
                        }
                        var value = data[ name ];
                        buffer.push(
                            encodeURIComponent( name ) +
                            "=" +
                            encodeURIComponent( ( value == null ) ? "" : value )
                        );
                    }
 
                    // Serialize the buffer and clean it up for transportation.
                    var source = buffer
                        .join( "&" )
                        .replace( /%20/g, "+" )
                    ;
                    return( source );
                }
            }
        );


GasistaFelice.config(['$routeProvider',function($routeProvider) {
		$routeProvider
    
            // route for the home page
        .when('/:pe/', {
				templateUrl : 'app/ordinare/ordinare.html',
				controller  : 'orderController'
			})

			// route for the paniere page
			.when('/:pe/paniere', {
				templateUrl : 'app/paniere/paniere.html',
				controller  : 'paniereController'
			})

			// route for the scheda page
            .when('/:pe/scheda', {
				templateUrl : 'app/scheda/scheda.html',
				controller  : 'schedaController'
			})
    
            // route for the conto page
            .when('/:pe/conto', {
				templateUrl : 'app/conto/conto.html',
				controller  : 'contoController'
			})
            .otherwise({
                    redirectTo: '/'
                });
	}]);

function wrapcontroller($scope,$http,$rootScope,$window,$routeParams){
	$scope.pe = {};
    $rootScope.peID = $routeParams.pe;
    $window.location.href = '#/'+$rootScope.peID+'/ordinare';
    console.log("CIAOCIAO!");
}



function gas_controller($scope, $http, $routeParams,$rootScope, $location){
    $scope.gasnames = [];
    $scope.selectedIndex = 0;
    
    $scope.itemClicked = function ($index) {
        $scope.selectedIndex = $index;
    }
    
    $scope.getID = function(gasname){
        $rootScope.gasID = gasname;
        console.log("Questo è il routeparams! " + $routeParams.pe);
        $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data) {
            $.each(data.gas_list, function(index, element){
            $.each(data.gasmembers, function(index2,element2){
                 $http.get('/gasistafelice/api/v1/gasmember/'+element2+'/?format=json').success(function(data){ 
                    console.log("CIAOCIAO!");
                 });
                });
            });
        });
    }
    
    var peID = $location.path().substring(1,3);
    
    //la get viene fatta in base all'utente - rootScope.personID dopo il login
    $http.get('/gasistafelice/api/v1/person/'+peID+'/?format=json').success(function(data) {
        $scope.gasmembers = [];
        $scope.balance = [];
        
        $.each(data.gasmembers, function (index,element){
            $scope.gasmembers.push({id:element});
        });
        
        i = 0;
        
        $.each(data.gas_list, function(index, element){
            $.each(data.gasmembers, function(index2,element2){
                 $http.get('/gasistafelice/api/v1/gasmember/'+element2+'/?format=json').success(function(data){ 
                     $scope.balance.push({balance: data.balance});
                     console.log("Ecco il balance preso dal json " + data.balance);
                     console.log($scope.balance);
                      $scope.gasnames.push({
                        id: element.id,
                        name: element.name,
                        balance: parseFloat(data.balance,10)
                    });
                 });
            });
            
            i = i + 1;
        });
    });
}

/*function controllerScheda($scope, $http, $routeParams,$rootScope, $location){
        $http.get('/gasistafelice/api/v1/person/'+peID+'/?format=json').success(function(data) {
                $scope.name = data.name;
        });
}*/

function menu_controller($scope,$http, $routeParams, $rootScope){
    $scope.gmID = $rootScope.gasmemberID;
}




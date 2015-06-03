var GasistaFelice = angular.module('ngGasistaFelice', [
    'ui.bootstrap',
    'ngRoute',
    'ngDialog',
    'ngLocale'
]).run(
    
  function($rootScope, $routeParams, $location, $http) {

    $rootScope.app_name = $.app_name;
    $rootScope.static_url = $.static_url;

    $rootScope.absurl_pre = $.absurl_pre;
    $rootScope.absurl_static = $.absurl_static;
    $rootScope.absurl_api = $.absurl_api;

    //Default values for page
    $rootScope.gas_id = $.default_gas_id;
    $rootScope.gasmember_id = $.default_gasmember_id;
    $rootScope.person_id = $.person_id;



    //TODO TOREMOVE
    $rootScope.gasmemberID = $.default_gasmember_id;
    $rootScope.peID = $.person_id;
    $rootScope.gasID = $.default_gas_id;

});

GasistaFelice.directive('validPrice',function() {
    return {
        require: "ngModel",
        link: function(scope, elm, attrs, ctrl){
            
            var regex=/^\d{2,4}(\.\d{1,2})?$/;
            ctrl.$parsers.unshift(function(viewValue){
                var floatValue = parseFloat(viewValue);
                if( floatValue >= 50 && floatValue <=5000 && regex.test(viewValue)){
                    ctrl.$setValidity('validPrice',true);
                    //return viewValue;
                }
                else{
                    ctrl.$setValidity('validPrice',false);
                }
                return viewValue;
            });
        }
    };
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
                return( ( data === null ) ? "" : data.toString() );
            }

            var buffer = [];
            // Serialize each key in the object.
            var i;
            for ( i=0; i<data.length; i++ ) {
                var name = data[i];
                if ( ! data.hasOwnProperty( name ) ) {
                    continue;
                }
                var value = data[ name ];
                buffer.push(
                    encodeURIComponent( name ) +
                    "=" +
                    encodeURIComponent( ( value === null ) ? "" : value )
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
    .when('/ordinare/:gasmember_id', {
        templateUrl : $.absurl_static+'app/ordinare/ordinare.html',
        controller  : 'orderController',
        resolve     : orderController.resolve
    })


    // route for paniere page
    .when('/paniere/:gasmember_id', {
        templateUrl : $.absurl_static+'app/paniere/paniere.html',
        controller  : 'paniereController',
        resolve     : paniereController.resolve
    })

    // route for scheda page
    .when('/scheda/:gasmember_id', {
        templateUrl : $.absurl_static+'app/scheda/scheda.html',
        controller  : 'schedaController',
        resolve     : schedaController.resolve
    })

    // route for conto page
    .when('/conto/:gasmember_id', {
        templateUrl : $.absurl_static+'app/conto/conto.html',
        controller  : 'contoController',
        resolve     : contoController.resolve
    })
    .otherwise({
        redirectTo: '/ordinare/'+$.default_gasmember_id //TODO: should be $rootScope.gasmember_id
    });
}]);

function wrapcontroller($scope,$http,$rootScope,$window,$routeParams){
	$scope.pe = {};
}


/* TODO TOREMOVE to be removed if not useful for the stable version
 * function gas_controller($scope, $http, $routeParams,$rootScope, $location, parsingNumbers, $q, person) {

    $rootScope.gasnames = [];
    $scope.selectedIndex = 0;
    
    $scope.itemClicked = function ($index) {
        $scope.selectedIndex = $index;
    };
    
    $scope.getID = function(gas_id){
        $rootScope.gasID = gas_id;
    };
        
    $scope.gasmembers = [];
    $scope.balance = [];

    person.get_info($q, $http).then(
      function (data) {

        $scope.person_name = data.name;
        
        $.each(data.gasmembers, function (index,element){
            $scope.gasmembers.push({id:element});
        });
        
        indice = 0;
        prova = 0;
        $.each(data.gas_list, function(index, element){
            indice = indice + 1;
            $.each(data.gasmembers, function(index2,element2){
                prova = prova + 1;
                if (indice == prova)
                {
                    $http.get($.absurl_api+'gasmember/'+element2+'/?format=json').success(function(data){ 
                     $scope.balance.push({balance: data.balance});
                     $rootScope.gasnames.push({
                            id: element.id,
                            name: element.name,
                            balance: parsingNumbers.parsing(data.balance,2)
                        });
                    });
                    
                    prova = 0;
                    indice = indice + 1;
                }
            });
        });    
    });
}
*/

function menu_controller($scope,$http, $routeParams, $rootScope){
    $scope.gmID = $rootScope.gasmemberID;
}

GasistaFelice.config(function($httpProvider) {

    // Use x-www-form-urlencoded Content-Type
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

    // Override $http service's default transformRequest
    $httpProvider.defaults.transformRequest = [function(data)
    {      
         var param = function(obj) {
            var query = '';
            var name, value, fullSubName, subValue, innerObj, i, split, counter;

                for (name in obj) {
                    value = obj[name];

                    if (value instanceof Array) {
                        for (var i = 0; i < value.length; ++i) {
                        counter = i;
                        subValue = value[i];
                        fullSubName = name + '-' + i + '-';
                        innerObj = {};
                        innerObj[fullSubName] = subValue;
                        query += param(innerObj) + '&';
                        }
                    } else if (value instanceof Object) {
                        for (var subName in value) {
                            subValue = value[subName];
                            
                            if (subName == "TOTAL_FORMS" || subName=="INITIAL_FORMS" || subName=="MAX_NUM_FORMS")
                            {    
                                 fullSubName = "form-" + subName;
                            }
                            else{
                                fullSubName = name + subName;
                            }
                            
                            innerObj = {};
                            innerObj[fullSubName] = subValue;
                            query += param(innerObj) + '&';
                        }
                    } else if (value !== undefined && value !== null) {
                    query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
                    }
                }
            return query.length ? query.substr(0, query.length - 1) : query;
            }
        return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
    }];

}); 

 
GasistaFelice.service('gettingValues', function () {
    this.pull = function(){
    }
});

GasistaFelice.service('parsingNumbers', function() {
    this.parsing = function(number,d) {
        if (d >= 0)
        {
            return parseFloat(number).toFixed(d);
        }
        else
        {
            return parseFloat(number,10);
        }
        
    };
});

GasistaFelice.service('person', function() {

    this.data = null;
    var this_svc = this;

    this.get_info = function($q, $http) {

        var deferred = $q.defer();
        if (this_svc.data === null) {
            $http.get($.absurl_api+'person/my/?format=json')
            .success(function(data) {
                this_svc.data = data;
                deferred.resolve(data);
            }).error(function(data){
                deferred.resolve("http error get person data");
            });
        } else
            deferred.resolve(this_svc.data);
            
        return deferred.promise;

     }

});

GasistaFelice.base_resolver = {

    get_person_data : function($q, $http, person) {
        return person.get_info($q, $http);
    }

}


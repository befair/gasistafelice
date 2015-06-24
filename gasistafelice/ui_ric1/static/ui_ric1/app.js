// Gasista Felice frontend evolved from a master thesis by Riccard1
//
var app = angular.module('ngGF', 
    [ 'ui.bootstrap', 'ngNewRouter', 'ngDialog', 'ngLocale' ]
    )
    .controller("AppController", function($http, $router, $rootScope, $location) {

        //TODO: settings
        $rootScope.app_name = app_name;
        $rootScope.static_url = static_url;

        $rootScope.absurl_pre = absurl_pre;
        $rootScope.absurl_static = absurl_static;
        $rootScope.absurl_api = absurl_api;

        //Default values for page
        $rootScope.gas_id = default_gas_id;
        $rootScope.gm_id = default_gasmember_id;
        $rootScope.gm = null;
        $rootScope.person_id = person_id;

        this.dataLoaded = false;
        var THAT = this;

        //TODO TOREMOVE
        $rootScope.gasmemberID = default_gasmember_id;
        $rootScope.peID = person_id;
        $rootScope.gasID = default_gas_id;
        //END TOREMOVE
        
        $http.get($rootScope.absurl_api+'person/my/?format=json')
            .success(function(data) {
                $rootScope.person = data;
                THAT.dataLoaded = true;
            }).error(function(data){
                alert("http error get person data");
            });

        $router.config([
            { path: "/order/", component: "order", as: "order" },
            { path: "/basket/", component: "basket", as: "basket" },
            { path: "/cash/", component: "cash", as: "cash" },
            { path: "/profile/", component: "profile", as: "profile" },
            { path: '/', redirectTo: "/order/" }
        ]);
        //$location.path('/'); //set default otherwise is blank
    })
    .service('parsingNumbers', function() {
        this.parsing = function(number,d) {
            if (d >= 0) {
                return parseFloat(number).toFixed(d);
            } else {
                return parseFloat(number,10);
            }

        };
    })
    .service('productManager', function($http, $rootScope, parsingNumbers) {

        //this.gm = $rootScope.gm;
        this.products = [];
        var THAT = this;

        //Store ordered products info by gsop_id
        this.ordered_products_d = {};

        this.set_ordered_products_from_basket = function (basket) {
            angular.forEach(basket, function(gmo, index) {
                var gsop = gmo.ordered_product;
                var min_amount = parsingNumbers.parsing(gsop.stock.detail_minimum_amount);
                var step_unit = parsingNumbers.parsing(gsop.stock.detail_step);
                var order_state = gsop.order.current_state.toLowerCase();

                this.ordered_products_d[gsop.id] = {
                    id : gsop.id,
                    price : parsingNumbers.parsing(gmo.ordered_price),
                    quantity: parsingNumbers.parsing(gmo.ordered_amount),
                    note : gmo.note,
                    name : gsop.stock.product.__unicode__,
                    supplier : gsop.order.supplier,
                    order_shortname : "Ord. " + gsop.order.id,
                    can_update : order_state == "open",
                    order_state : order_state,
                    step : step_unit,
                    min_amount : min_amount
                };
            }, THAT);
        };

        this.get_ordered_products = function () {
            //TODO REVIEW offline coding
            var ordered_products = [];
            angular.forEach(THAT.ordered_products_d, function(ordered_product, index) {
                ordered_products.push(ordered_product);
            });
            if (ordered_products.length === 0) {
                THAT.basket_empty = true;
            } else {
                THAT.basket_empty = false;
            }
            return ordered_products;
        };

        this.set_order_catalog = function(open_order, basket) {

            THAT.set_ordered_products_from_basket(basket);
            $rootScope.selected_order = open_order;
            THAT.products = [];

            angular.forEach(open_order.orderable_product_set, function(gsop) {

                var ordered_info = THAT.ordered_products_d[gsop.id];
                if (ordered_info === undefined) {
                    ordered_info = { price : null, quantity : 0, note : "" };
                }

                var el_prod = gsop.stock.product;
                var min_amount = parsingNumbers.parsing(gsop.stock.detail_minimum_amount);
                var step_unit = parsingNumbers.parsing(gsop.stock.detail_step);

                // console.debug("Adding product " + el_prod.__unicode__ + " to open order "+ open_order.id+"...");

                THAT.products.push({
                    id: gsop.id,
                    category: el_prod.category,
                    name: el_prod.__unicode__,
                    price: gsop.stock.price,
                    step: step_unit,
                    min_amount: min_amount,
                    quantity: ordered_info.quantity,
                    note: ordered_info.note
                });

                console.debug("done.");
            });
        };

        this.increment = function(product) {
            if (product.quantity === 0) {
                product.quantity += product.min_amount;
                console.debug("Increment to min_amount for product " + product.name);
            } else {
                product.quantity += product.step;
                console.debug("Increment of "+ product.step + "=" + product.quantity + " for product " + product.name);
            }
        };

        this.change = function(product) {
            // Check if value is not under the minimum amount and
            // adjust the value if not in the right "tick" of min_amount + step
            if (product.quantity !== 0) {
                if (product.quantity < product.min_amount) {
                    alert("La quantità minima per questo prodotto è "+ product.min_amount);
                    product.quantity = product.min_amount;
                } else if ((product.quantity-product.min_amount)%product.step !== 0) {
                    var base = product.quantity-product.min_amount;
                    var next_step_allowed = parseInt(base/product.step, 10)*product.step+product.step+product.min_amount;
                    alert("Puoi ordinare " + (next_step_allowed-product.step) + " o " + next_step_allowed + " " + product.name + " ma non " + product.quantity);

                    product.quantity = next_step_allowed;
                }
            }
        };

        this.decrement = function(product) {
            if (product.quantity === product.min_amount || product.quantity === 0) {
                product.quantity = 0;
            } else if (product.quantity === 0) {
                product.quantity = 0;
            } else {
                product.quantity -= product.step;
            }
        };

        this.getTotal = function(products) {
            var total = 0, i;
            for(i = 0; i < products.length; i++) {
                var product = products[i];
                total += (product.price * product.quantity);
            }
            return parseFloat(total).toFixed(2);
        };

        this.updateBasket = function() {
          
            var products_post = [];

            angular.forEach(THAT.products, function(product, i) {

                //FORMATTING products for the POST
                products_post.push({
                    id: "",
                    gsop_id: product.id,
                    ordered_price: product.price,
                    ordered_amount: product.quantity,
                    note: product.note
                });
            });

            products_post.push({
                "TOTAL_FORMS": products_post.length,
                "INITIAL_FORMS": 0,
                "form-MAX_NUM_FORMS": ""
            });
            
            var POST_order_path = $rootScope.absurl_pre+'rest/gasmember/'+$rootScope.gm_id+'/order/edit_multiple';
            $http.post(POST_order_path, { form: products_post })
                .success(function(){
                    alert("Prodotti aggiunti al paniere con successo!");
                })
                .error(function(){
                    alert("C'è stato qualche problema, riprova");
                });
        };

    })
    .directive('validPrice',function() {
        return {
            require: "ngModel",
            link: function(scope, elm, attrs, ctrl) {
                
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
    }).factory(
        "transformRequestAsFormPost", function() {

            // ---
            // PRIVATE METHOD.
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

            // PUBLIC INTERFACE
            // I prepare the request data for the form post.
            function transformRequest( data, getHeaders ) {
                var headers = getHeaders();
                headers[ "Content-type" ] = "application/x-www-form-urlencoded; charset=utf-8";
                return( serializeData( data ) );
            }
            // Return the factory value.
            return( transformRequest );
    })
    .config(["$httpProvider", function($httpProvider) {

        // Use x-www-form-urlencoded Content-Type
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

        // Override $http service's default transformRequest
        $httpProvider.defaults.transformRequest = [ function(data) {      
            var param = function(obj) {
                var query = '';
                var name, value, fullSubName, subValue, innerObj, i, split, counter, subName;

                for (name in obj) {
                    value = obj[name];

                    if (value instanceof Array) {
                        for (i = 0; i < value.length; ++i) {
                            counter = i;
                            subValue = value[i];
                            fullSubName = name + '-' + i + '-';
                            innerObj = {};
                            innerObj[fullSubName] = subValue;
                            query += param(innerObj) + '&';
                        }
                    } else if (value instanceof Object) {
                        for (subName in value) {
                            subValue = value[subName];
                            
                            if (subName == "TOTAL_FORMS" || subName=="INITIAL_FORMS" || subName=="MAX_NUM_FORMS") {    
                                fullSubName = "form-" + subName;
                            } else { 
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
            };
            return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
        }];

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

function menu_controller($scope,$http, $routeParams, $rootScope){
    $scope.gmID = $rootScope.gasmemberID;
}
*/


/*app.base_resolver = {

    person_data : function($q, $http, person) {
        return person.get_info($q, $http);
    }

}*/


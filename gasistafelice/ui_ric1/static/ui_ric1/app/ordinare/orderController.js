function orderController($scope,$http,$rootScope, $routeParams, $timeout, parsingNumbers, $locale){

    $scope.dataLoaded = true;
    $scope.ordiniloaded = true;
    $scope.orderByField = '';
    $scope.reverseSort = false;
    $scope.POST_order_path = $.absurl_pre+'rest/gasmember/'+$routeParams.gasmember_id+'/order/edit_multiple';
          
    var data = $rootScope.gasmember; 
    var gas_id = data.gas;

    $scope.balance = parsingNumbers.parsing(data.balance,2);  
    $scope.tb = parsingNumbers.parsing(data.total_basket);
    $scope.tbtbd = parsingNumbers.parsing(data.total_basket_to_be_delivered);
    var appo = $scope.tb + $scope.tbtbd;
    $scope.resume = $scope.balance - appo;
    $scope.resume = parsingNumbers.parsing($scope.resume,2);

        
    $scope.open_orders = data.open_orders;
    $scope.products = [];
    $scope.products_post = [];

    $scope.set_order_catalog = function(order_id) {

        $scope.products = [];
        $scope.products_post = [];
        $rootScope.order_id = order_id;

        $.each(data.open_orders, function(index, order) {
            if (order_id == order.id) {
                $.each(order.orderable_product_set, function(index, gsop) {

                    prodel = gsop.stock.product;
                    minamount = parsingNumbers.parsing(gsop.stock.detail_minimum_amount);
                    stepunit = parsingNumbers.parsing(gsop.stock.detail_step);
                    $scope.products.push({
                        id: gsop.id,
                        category: prodel.category,
                        name: prodel.name,
                        price: gsop.stock.price,
                        desc: prodel.description,
                        mu:prodel.mu,
                        pu:prodel.pu,
                        quantity: 0,
                        step: stepunit,
                        //total_price: minamount * stocklist.price,
                        total_price: 0,
                        note: ""
                    });
                    //LOADING products for the POST
                    $scope.products_post.push({
                        id: "",
                        gsop_id: gsop.id,
                        ordered_price: gsop.stock.price,
                        ordered_amount: 0,
                        note: ""
                    });
                });
            }
        });
    };

    $scope.set_order_catalog(data.open_orders[0].id);

    $scope.increment = function(product,i){
        quantity = parsingNumbers.parsing(product.quantity);
        quantity += product.step;
        product.quantity = quantity;
        product.total_price = quantity * product.price;
        $scope.products_post[i].ordered_amount += product.step;
        //console.log($scope.products_post[i].ordered_amount);
    };

    $scope.change = function(product,i){
        quantity = parsingNumbers.parsing(product.quantity);
        product.total_price = quantity * product.price;
        $scope.products_post[i].ordered_amount = quantity;
        console.log(quantity);
        //console.log($scope.products_post[i].ordered_amount);
    };

    $scope.decrement = function(product,i){
        quantity = parsingNumbers.parsing(product.quantity);
        console.log(quantity);
        sum = quantity - product.step;
        console.log(sum);
        if (sum > -1) {
            product.quantity -= product.step;
            $scope.products_post[i].ordered_amount -= product.step;
            product.total_price = product.quantity * product.price;
        }
    };

    $scope.getTotal = function(){
        var total = 0;
        for(var i = 0; i < $scope.products.length; i++) {
            var product = $scope.products[i];
            total += (product.price * product.quantity);
        }
        return parseFloat(total).toFixed(2);
    }

    $scope.submitData = function(){
      
        angular.forEach($scope.products, function(index , element) {
            console.log(element);
            try{
             $scope.products_post[element].note = index.note;   
            }
            catch(err)
            {
                
            }
        })
            $scope.products_post.push({
                TOTAL_FORMS:$scope.products_post.length,
                INITIAL_FORMS:0,
                MAX_NUM_FORMS:""
            });
        
        $http.post($scope.POST_order_path, {form:$scope.products_post})
        .success(function(){
             $scope.products_post.splice($scope.products_post.length - 1 , 1);                                      
            alert("Prodotti aggiunti al paniere!");
        })
        .error(function(){
               $scope.products_post.splice($scope.products_post.length - 1, 1);   
            alert("C'è stato qualche problema, riprova");
        });
    };
    
 
}

orderController.resolve = GasistaFelice.base_resolver;
orderController.resolve.r_gasid = function($q, $http, $routeParams, $route, $rootScope) {

    var deferred = $q.defer();
    var gm_id = $route.current.params.gasmember_id;
    $http.get($.absurl_api+'gasmember/'+ gm_id +'/?format=json')
    .success(function(data) {
        $rootScope.gasmember = data;
        deferred.resolve(data);
    })
    .error(function(data){
        deferred.resolve("error value");
    });

    return deferred.promise;
}


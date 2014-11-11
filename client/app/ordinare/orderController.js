function orderController($scope,$http,$rootScope, $routeParams, $timeout, r_gasid, parsingNumbers, $locale){

  $scope.dataLoaded = "false";
  $scope.ordiniloaded = "false";
  $scope.orderByField = '';
  $scope.reverseSort = false;
  $rootScope.peID = $routeParams.pe;
          
  $http.get('/gasistafelice/api/v1/gasmember/'+$rootScope.gasmemberID+'/?format=json').success(function(data){
      $scope.balance = parsingNumbers.parsing(data.balance,2);  
      $scope.tb = parsingNumbers.parsing(data.total_basket);
      $scope.tbtbd = parsingNumbers.parsing(data.total_basket_to_be_delivered);
      var appo = $scope.tb + $scope.tbtbd;
      $scope.resume = $scope.balance - appo;
      $scope.resume = parsingNumbers.parsing($scope.resume,2);
  });
    
  $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
    $scope.gasmemberid = data.id;
    $scope.path = '/gasistafelice/rest/gasmember/'+$rootScope.gasmemberID+'/order/edit_multiple';
 });

    
 var gasid = $rootScope.gasID; //DEFAULT VALUE 
        
 $scope.openorders = [];
 $scope.products = [];
 $scope.products_post = [];
    
 $scope.getsupplyID = function(supplyID){
    
    $scope.prodnumber = 0;
    $scope.products = [];
    $scope.products_post = [];
    $scope.dataLoaded = "false";
    $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
    $.each(data.gas_list, function(index, element){
        $.each(element.open_orders, function(index, element){
                if (supplyID == element.supplier)
                {
                    $.each(element.orderable_product_set, function(index, order)
                    {
                        gsopid = order.id;
                        gasstock = order.gasstock;
                        $.each(element.gasstock_set, function(index, gas)
                        {
                            if (gas.id == gasstock)
                            {
                                $scope.stock = gas.stock;
                                $.each(element.stocks, function(index, stocklist)
                                {
                                 if (stocklist.id == $scope.stock)
                                 {    
                                     minamount = parsingNumbers.parsing(gas.minimum_amount);
                                     stepunit = parsingNumbers.parsing(gas.step);
                                     $scope.prodnumber = $scope.prodnumber + 1;
                                     prodel = stocklist.product;
                                     //LOADING products for the VIEW
                                     $scope.products.push({
                                         id: gsopid,
                                         category: prodel.category,
                                         name: prodel.name,
                                         price: stocklist.price,
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
                                         gsop_id: gsopid,
                                         ordered_price: stocklist.price,
                                         ordered_amount: 0,
                                         note: ""
                                     });
                                 }        
                                });
                            }
                        });
                    });
                }
        });
    });
      $scope.dataLoaded = "true";  
    });
     
      
};
  
 //LOADING ORDERS
 //TODO - gestione id persona (tramite rootscope o service)
 
// $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
//    $scope.person = data;
//    $scope.supplier = [];
//    $.each(data.gas_list, function(index, element){
//        if (element.id == gasid)
//        {
//            $scope.openorders = element;
//            $.each(element.open_orders, function(index, element){
//                $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(gf_person){
//                  $.each(gf_person.suppliers, function(index,supply){
//                        if (supply.id == element.supplier) 
//                        {    
//                            $scope.supplier.push({name:supply.name});
//                        } 
//                  });
//                });
//                if ($rootScope.first == true){
//                    $rootScope.supplyID = element.supplier;
//                    $rootScope.first = false;
//                    $scope.dataLoaded = "true";
//                }
//                
//                if ($rootScope.supplyID == element.supplier)
//                {
//              	         $.each(element.gasstock_set, function(index, product)
//                         {
//                             stock = product.stock;
//                             $.each(element.stocks, function(index2, product2)
//                             {
//                                 if (product2.id == stock)
//                                 {    
//                                     minamount = parseFloat(product.minimum_amount,10);
//                                     stepunit = parseFloat(product.step,10);
//                                     prodel = product2.product;
//                                     $scope.products.push({
//                                         id: prodel.id,
//                                         category: prodel.category,
//                                         name: prodel.name,
//                                         price: product2.price,
//                                         desc: prodel.description,
//                                         mu:prodel.mu,
//                                         pu:prodel.pu,
//                                         quantity: 0,
//                                         step: stepunit,
//                                         total_price: minamount * product2.price,
//                                         note: ""
//                                     });
//                                     //LOADING products for the POST
//                                     $scope.products_post.push({
//                                         id: "",
//                                         gsop_id: prodel.id,
//                                         ordered_price: product2.price,
//                                         ordered_amount: 0,
//                                         note: ""
//                                     });
//                                 }
//                                 
//                             });
//                         });    
//                }
//            });
//        } 
//     }); 
//      
//$scope.ordiniloaded = "true";
// });
    
    
 $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
    $scope.prodnumber = 0;
    $scope.person = data;
    $scope.supplier = [];
    $.each(data.gas_list, function(index, element){
        if (element.id == gasid)
        {
            $scope.openorders = element;
            $.each(element.open_orders, function(index, element){
                $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(gf_person){
                  $.each(gf_person.suppliers, function(index,supply){
                        if (supply.id == element.supplier) 
                        {    
                            $scope.supplier.push({name:supply.name});
                        } 
                  });
                });
                if ($rootScope.first == true){
                    $rootScope.supplyID = element.supplier;
                    $rootScope.first = false;
                    $scope.dataLoaded = "true";
                }
                
                if ($rootScope.supplyID == element.supplier)
                {
                     $.each(element.orderable_product_set, function(index, order)
                    {
                        gsopid = order.id;
                        gasstock = order.gasstock;
                        $.each(element.gasstock_set, function(index, gas)
                        {
                            if (gas.id == gasstock)
                            {
                                $scope.stock = gas.stock;
                                $.each(element.stocks, function(index, stocklist)
                                {
                                 if (stocklist.id == $scope.stock)
                                 {    
                                     minamount = parsingNumbers.parsing(gas.minimum_amount);
                                     stepunit = parsingNumbers.parsing(gas.step);
                                     $scope.prodnumber = $scope.prodnumber + 1;
                                     prodel = stocklist.product;
                                     //LOADING products for the VIEW
                                     $scope.products.push({
                                         id: gsopid,
                                         category: prodel.category,
                                         name: prodel.name,
                                         price: stocklist.price,
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
                                         gsop_id: gsopid,
                                         ordered_price: stocklist.price,
                                         ordered_amount: 0,
                                         note: ""
                                     });
                                 }        
                                });
                            }
                        });
                    });
                }
            });
        } 
     }); 
      
$scope.ordiniloaded = "true";
 });
    
    
    
    

    
    $scope.increment = function(product,i){
        quantity = parsingNumbers.parsing(product.quantity);
        quantity += product.step;
        product.quantity = quantity;
        product.total_price = quantity * product.price;
        $scope.products_post[i].ordered_amount += product.step;
        //console.log($scope.products_post[i].ordered_amount);
    }
    
    $scope.change = function(product,i){
        quantity = parsingNumbers.parsing(product.quantity);
        product.total_price = quantity * product.price;
        $scope.products_post[i].ordered_amount = quantity;
        console.log(quantity);
        //console.log($scope.products_post[i].ordered_amount);
    }
    
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
    }
    
    $scope.getTotal = function(){
    var total = 0;
        for(var i = 0; i < $scope.products.length; i++){
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
            $scope.products_post.push({TOTAL_FORMS:$scope.prodnumber,
                                   INITIAL_FORMS:0,
                                    MAX_NUM_FORMS:""});
        
        $http.post($scope.path, {form:$scope.products_post})
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

orderController.resolve = {
    r_gasid : function($q, $http, $routeParams, $route, $rootScope) {
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



 

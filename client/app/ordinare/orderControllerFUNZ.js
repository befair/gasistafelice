function orderController($scope,$http,$rootScope, $routeParams){

  // $scope.supplyname = ["La Terra e il Cielo", "Daloisio Agrumi", "Collestefano", "Tea Natura"];
    
  $scope.orderByField = '';
  $scope.reverseSort = false;
  $rootScope.peID = $routeParams.pe;
  console.log($rootScope.gasmemberID);
  console.log("Scope condiviso " + $rootScope.peID);
  $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
    $scope.tb = data.total_basket;
    $scope.tbtbd = data.total_basket_to_be_delivered;
    $scope.balance = data.balance;
    $scope.gasmemberid = data.id;
    $scope.path = '/gasistafelice/rest/gasmember/'+$scope.gasmemberid+'/order/edit_multiple';
 });

    
 var gasid = $rootScope.gasID; //DEFAULT VALUE 
    
 $scope.openorders = [];
 $scope.products = [];
  
 $scope.getsupplyID = function(supplyID){
    $scope.products = [];
    $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
    $.each(data.gas_list, function(index, element){
        $.each(element.open_orders, function(index, element){
                if (supplyID == element.supplier)
                {
			     $.each(element.gasstock_set, function(index, product)
                        {
                            stock = product.stock;
                            $.each(element.stocks, function(index2, product2)
                            {
                                if (product2.id == stock)
                                {    
                                    minamount = parseFloat(product.minimum_amount,10);
                                    stepunit = parseFloat(product.step,10);
                                    prodel = product2.product;
                                    $scope.products.push({
                                        id: prodel.id,
                                        category: prodel.category,
                                        name: prodel.name,
                                        price: product2.price,
                                        desc: prodel.description,
                                        mu:prodel.mu,
                                        pu:prodel.pu,
                                        quantity: minamount,
                                        step: stepunit,
                                        total_price: minamount * product2.price
                                    });
                                }        
                            });
                        });    
                }
        });
    });
    });
};

  
 //LOADING ORDERS
 //TODO - gestione id persona (tramite rootscope o service)
 $http.get('/gasistafelice/api/v1/person/'+$routeParams.pe+'/?format=json').success(function(data){
    $scope.person = data;
    $.each(data.gas_list, function(index, element){
        if (element.id == gasid)
        {
            $scope.openorders = element;
            $.each(element.open_orders, function(index, element){
                if ($rootScope.first == true){
                    $rootScope.supplyID = element.supplier;
                    $rootScope.first = false;
                }
                
                if ($rootScope.supplyID == element.supplier)
                {
              	$.each(element.gasstock_set, function(index, product)
                 //        $.each(element.orderable_product_set, function(index, product)
                         {
                             stock = product.stock;
                             $.each(element.stocks, function(index2, product2)
                             {
                                 if (product2.id == stock)
                                 {    
                                     minamount = parseFloat(product.minimum_amount,10);
                                     stepunit = parseFloat(product.step,10);
                                     prodel = product2.product;
                                     $scope.products.push({
                                         id: prodel.id,
                                         category: prodel.category,
                                         name: prodel.name,
                                         price: product2.price,
                                         desc: prodel.description,
                                         mu:prodel.mu,
                                         pu:prodel.pu,
                                         quantity: minamount,
                                         step: stepunit,
                                         //total_price: parseFloat((minamount * product2.price),10).toFixed(1)
                                         total_price: minamount * product2.price
                                     });
                                 }
                                 
                             });
                         });    
                }
            });
        } 
     });   
 });

    $scope.increment = function(product){
        product.quantity += product.step;
        product.total_price = product.quantity * product.price;
    }
    
    $scope.decrement = function(product){
        sum = product.quantity - product.step;
        if (sum > -1) {
            product.quantity -= product.step;
            product.total_price = product.quantity * product.price;
        }
    }
    
    $scope.getTotal = function(){
    var total = 0;
        for(var i = 0; i < $scope.products.length; i++){
            var product = $scope.products[i];
            total += (product.price * product.quantity);
        }
    return total;
    }   
 }

function FrmController($scope,$http,transformRequestAsFormPost){
                $scope.form = {};
                $scope.addtoCart = function() {
                    $http({
                        method: 'POST',
                        url: '',
                        //transformRequest: transformRequestAsFormPost,
                        data: $.param($scope.form),
                        headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                    });
                }
}


 
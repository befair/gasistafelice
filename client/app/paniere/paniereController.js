function paniereController($scope,$http,$rootScope, $sce){
$scope.btbd = [];
$scope.orderByField = '';
$scope.reverseSort = false;
    
//URL per la GET del PANIERE -> http://gasistafelice.befair.it:8001/gasistafelice/rest/gasmember/20/basket/edit_multiple
    

var pathGet = "http://gasistafelice.befair.it:8001/gasistafelice/rest/gasmember/"+$rootScope.gasmemberID+"/basket/edit_multiple";
console.log(pathGet);
var order = "";
var suppliername = "";
var productname = "";
var ordprice = "";
var ordamount = "";
$scope.basket = [];
var index = 1;
var value = "";
$scope.path="/gasistafelice/rest/gasmember/"+ $rootScope.gasmemberID+"/basket/edit_multiple";
//use $rootScope.gasmemberID to get the right JSON
    
$scope.dataLoaded = "false";
$scope.prodnumber = 0;
$http.get('/gasistafelice/rest/gasmember/'+$rootScope.gasmemberID+'/basket/edit_multiple?render_as=table&iDisplayLength=-1').success(function(data){
      console.log("CIAOCIAO!");
      $.each(data.aaData, function(index, basket){
          value = basket[6].indexOf("value");
          step = basket[6].indexOf("step");
	  console.log("CIAO!" + basket[0]);
          if ($.isNumeric(basket[6].substr(value+7,2)))
          {
            index = 2;
            amount = basket[6].substr(value+7,2);
          }
          else{
            amount = basket[6].substr(value+7,1);
          }
          $scope.basket.push({
			id: basket[0].substring(0,6),
                        order: basket[1],
                        supplier: basket[2],
                        //product: basket[3],
			            gm: $rootScope.gasmemberID,
                        price: parseFloat(basket[4].substring(13,8)),
                        amount: parseFloat(amount),
                        //total: parseFloat(amount)*parseFloat(basket[4].substring(13,8)),
                        total: amount * parseFloat(basket[4].substring(13,8)),
                        step: parseFloat(basket[6].substr(step+6,1)),
                        delete: "false"});
          $scope.prodnumber = $scope.prodnumber + 1;
      });
	$scope.dataLoaded = "true";
 });    

$scope.delete = function ( idx ) {
  var person_to_delete = $scope.basket[idx];
  $scope.basket.splice(idx, 1);
};
    
//BTBD getting data
$http.get('./lib/gasmemberNEW.json').success(function(data){
      $.each(data.basket_to_be_delivered, function(index, basket){
            order = basket.ordered_product.order;
            suppliername = basket.supplier.name;
            productname = basket.ordered_product.gasstock.stock.product.name;
            ordprice = basket.ordered_price;
            ordamount = basket.ordered_amount;
            total = ordprice * ordamount;
            $scope.btbd.push({order_id: order,
                              supplier: suppliername,
                              product: productname,
                              price: ordprice,
                              amount: ordamount,
                              total: total});
      });
 });
    
    $scope.increment = function(product){
        product.amount += product.step;
        product.total = parseFloat(product.amount * product.price,10);
    }
    
    $scope.decrement = function(product){
        sum = product.amount - product.step;
        if (sum > -1) {
            product.amount -= product.step;
            product.total = parseFloat(product.amount * product.price,10);
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
 
      
$scope.elimina = function(){
    console.log("PROVA");
     $scope.example =
       'I am an <code>HTML</code>string with ' +
       '<a href="#">links!</a> and other <em>stuff</em>';
    $scope.myHTML = $sce.trustAsHtml($scope.example);
   
}  

}



function FrmPaniereController($scope,$http,transformRequestAsFormPost){
                $scope.form = {};
                $scope.addtoCart = function() {
                    //http://beta.ordini.desmacerata.it/gasistafelice/rest/gasmember/514/order/edit_multiple
                    //localStorage["localproducts"] = JSON.stringify($scope.products);
                    //var appo = JSON.stringify($scope.data);
                    $http({
                        method: 'POST',
                        url: '',
                        //transformRequest: transformRequestAsFormPost,
                        data: $.param($scope.form),
                        headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                    });
                }
}

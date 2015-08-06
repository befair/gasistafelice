app.controller("BasketController", function ($http, $rootScope, parsingNumbers, productManager) {

    if (!$rootScope.gm_id) {
        console.debug("basket: GASMember info not already retrieved...");
        return;
    }

    $rootScope.active_section = "basket";

    this.pm = productManager;
    this.gm = $rootScope.gm;
    this.dataLoaded = true;

    this.sorting = ''; //basket table sorting name
    this.reverseSort = false; //basket table sorting
    this.tbd_sorting = ''; //basket to be delivered table sorting name
    this.tbd_reverseSort = false; //basket to be delivered table sorting

    this.open_ordered_products = [];
    this.closed_ordered_products = [];
    var THAT = this;


    this.get_ordered_products_from_basket = function(basket) {
        var products = [];
        angular.forEach(basket, function(gmo, index) {
            var gsop = gmo.ordered_product;
            var min_amount = parsingNumbers.parsing(gsop.stock.detail_minimum_amount);
            var step_unit = parsingNumbers.parsing(gsop.stock.detail_step);
            var order_state = gsop.order.current_state.toLowerCase();

            products.push({
                id : gmo.id,
                price : parsingNumbers.parsing(gmo.ordered_price),
                quantity: parsingNumbers.parsing(gmo.ordered_amount),
                note : gmo.note,
                name : gsop.stock.product.__unicode__,
                supplier : gsop.order.supplier,
                order_shortname : "Ord. " + gsop.order.id,
                can_update : order_state == "open",
                order_state : order_state,
                step : step_unit,
                min_amount : min_amount,
                gsop_id : gsop.id,
                enabled: false //flag to __remove__ a product from basket
            });
        });
        return products;
    };

    $http.get('/api/v1/gasmember/' + $rootScope.gm_id+'/?format=json')
    .success(function(data) {

        $rootScope.gm = data;
        var gm = $rootScope.gm;
        console.debug("Recuperato il paniere per " + gm.id);

        THAT.open_ordered_products = THAT.get_ordered_products_from_basket(gm.basket);
        THAT.closed_ordered_products = THAT.get_ordered_products_from_basket(gm.basket_to_be_delivered);

    }).error(function(data){
        console.debug("http error get GAS member data");
    });

    return;
});

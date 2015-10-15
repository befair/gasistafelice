app.controller("OrderController", function($http, $rootScope, productManager) {

    $rootScope.checkAuth();

    if (!$rootScope.gm_id) {
        console.debug("order: GASMember info not already retrieved...");
        return;
    }

    $rootScope.active_section = "order";

    this.pm = productManager;
    this.dataLoaded = true;

    this.ordiniloaded = true;
    this.orderByField = ''; //?
    this.reverseSort = false; //?

    $http.get('/api/v1/gasmember/' + $rootScope.gm_id+'/?format=json')
    .success(function(data) {

        $rootScope.gm = data;
        var gm = $rootScope.gm;
        console.debug('OrderController for gm=' + gm.id);

        if (gm.open_orders.length > 0) {
            console.debug("Setting the default order catalog...");
            productManager.set_order_catalog(gm.open_orders[0], gm.basket);
        } else {
            console.debug("Nessun ordine aperto per " + gm.gas.name);
        }

    }).error(function(data){
        console.debug("http error get GAS member data");
    });
});


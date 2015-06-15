app.controller("OrderController", function($http, $rootScope, $routeParams, productManager) {

    this.pm = productManager;
    this.gm = $rootScope.gm;
    this.dataLoaded = true;
    
    console.debug('OrderController for gm=' + this.gm.id);

    this.ordiniloaded = true;
    this.orderByField = ''; //?
    this.reverseSort = false; //?

    if (this.gm.open_orders.length > 0) {
        console.debug("Setting the default order catalog...");
        this.pm.set_order_catalog(this.gm.open_orders[0]);
    } else {
        alert("Nessun ordine aperto per "+this.gm.gas.name);
    }

});


app.controller("CashController", function($http, $rootScope, $routeParams) {

    console.debug('CashController for gm=' + $rootScope.gm_id);
    this.transactions = [];
    this.info = {};
    var THAT = this;

    this.get_cash_after_delivery = function() {
        return THAT.info.balance - THAT.info.total_basket - THAT.info.total_basket_to_be_delivered;
    };

    $http.get('/api/v1/gasmember/' + $rootScope.gm_id+'/cash/?format=json')
    .success(function (data) {
        THAT.transactions = data.economic_movements;
        THAT.info = data.cash_info;
    })
    .error(function (data) {
        //DEBUG
        alert("Error in retrieving economic movements, debug values loaded");
        THAT.transactions.push({
            id : 132,
            date: "21/07/2014 18:30",
            kind: 'decurtazione',
            amount: -70.00,
            details: "ordine 38 REC - Alchemia"
        });
        THAT.info = {
            balance : 30.00,
            total_basket : 20.00,
            total_basket_to_be_delivered : 10.00
        };
    });
});


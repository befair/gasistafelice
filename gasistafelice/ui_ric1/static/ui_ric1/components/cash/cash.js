app.controller("CashController", function($http, $rootScope, $routeParams) {

    console.debug('CashController for gm=' + $rootScope.gm_id);
    this.transactions = [];
    var THAT = this;

    $http.get($rootScope.absurl_api+'gasmember/' + $rootScope.gm_id+'/cash/?format=json')
    .success(function (data) {
        THAT.transactions = data.transactions;
    })
    .error(function (data) {
        THAT.transactions.push({
            id : 132,
            date: "21/07/2014 18:30",
            kind: 'decurtazione',
            amount: -70.00,
            details: "ordine 38 REC - Alchemia"
        });
    });
});


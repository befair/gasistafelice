angular.module('gettext').run(['gettextCatalog', function (gettextCatalog) {
/* jshint -W100 */
    gettextCatalog.setStrings('it', {"After delivery: {{ gm.balance - gm.total_basket_to_be_delivered - gm.total_basket | currency}}":"Dopo la consegna: {{ gm.balance - gm.total_basket_to_be_delivered - gm.total_basket | currency}}","Balance: {{ gm.balance | currency }}":"Saldo: {{ gm.balance | currency }}","Basket":"Paniere","Cash":"Conto","Just a moment please, I am loading...":"Un attimo, sto caricando...","Login":"Entra","Logout":"Esci","Manage":"Gestione","My profile":"Il mio profilo","Orders":"Ordini","password":"password","username":"utente","Welcome to the real world, Neo...!":"Benvenuto nel nuovo mondo...!"});
/* jshint +W100 */
}]);
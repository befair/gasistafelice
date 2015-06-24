app.controller("ProfileController", function ($http, $rootScope, ngDialog, parsingNumbers) {

    this.person = $rootScope.person;
    console.debug('profile '+ this.person.id);
    this.clickToOpen = function () {
        ngDialog.open({ 
            template: 'popupTemplate',
            className: 'ngdialog-theme-flat',
            scope: $rootScope
        });
    };
    
    return;
}); 

/* TODO DISASTER RECOVERY...
 *
        var id = $routeParams.id;
        $scope.path_gmid=$.absurl_api+"gasmember/"+$rootScope.gasmemberID+"/?format=json";
        $http.get($.absurl_api+'gasmember/'+$rootScope.gasmemberID+'/?format=json').success(function(data){
          $scope.balance = parsingNumbers.parsing(data.balance,2);  
          $scope.tb = parsingNumbers.parsing(data.total_basket);
          $scope.tbtbd = parsingNumbers.parsing(data.total_basket_to_be_delivered);
          var appo = $scope.tb + $scope.tbtbd;
          $scope.resume = $scope.balance - appo;
          $scope.resume = parsingNumbers.parsing($scope.resume,2);
        });
        
        $http.get($.absurl_api+'person/'+$routeParams.pe+'/?format=json').success(function(data){
            
              $.each(data.gas_list, function(index, element){
                $.each(data.gasmembers, function(index2,element2){
                 $http.get($.absurl_api+'gasmember/'+element2+'/?format=json').success(function(data){ 
                        $scope.tb = parsingNumbers.parsing(data.total_basket);
                        $scope.tbtbd = parsingNumbers.parsing(data.total_basket_to_be_delivered);
                        $scope.balance = parsingNumbers.parsing(data.balance);
                    });
                 });
              });            
            
            $scope.scheda = data;
            $.each(data.contact_set, function(index, element){
                $scope.contact = element;
                if (element.flavour == "EMAIL")
                {
                    $scope.email = element;
                }
                else
                {
                    $scope.phone = element;
                }     
            });
        });
*/

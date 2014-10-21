angular.module('ngGasistaFelice').controller('contoController', function($scope) {
		$scope.message = 'Contact us! JK. This is just a demo.';
          $(function() {
            $( '#datepicker' ).datepicker();
              console.log("CIAOCIAOCIAO");
          });
});

function formController($scope,$http,$rootScope, $sce){
    $scope.username1 = 'Peter Parker';
}

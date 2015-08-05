app.controller("LoginController", function($http, $rootScope, loginManager, $location) {

    var self = this;
    var next = $location.search().next;
    next = next === undefined ? '/' : next;
    var lm = loginManager;

    if (lm.isAuth()) {
        lm.load_person();
        $location.path(next);
    } else {
        lm.get_csrf_token();
    }

    this.login = function() {
        lm.login(self.username, self.password, next)
        .then(
            function(response) {
                lm.set_active_section(next);
            },
            function (data) {
                $rootScope.msg = 'Error';
            }
        );
    };
    this.isAuth = lm.isAuth;
});

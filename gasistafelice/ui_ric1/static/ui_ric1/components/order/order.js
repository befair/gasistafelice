app.controller("OrderController", function($http, $rootScope, $routeParams, parsingNumbers) {

    this.gm = $rootScope.gm;
    
    //Store ordered products info by gsop_id
    this.ordered_products_d = {};
    angular.forEach(this.gm.basket, function(gmo, index) {
        this.ordered_products_d[gmo.ordered_product.id] = {
            price : parsingNumbers.parsing(gmo.ordered_price),
            amount: parsingNumbers.parsing(gmo.ordered_amount),
            note : gmo.note
        };
    }, this);

    console.debug('OrderController for gm=' + this.gm.id);

    this.dataLoaded = true;
    this.ordiniloaded = true;
    this.orderByField = '';
    this.reverseSort = false;
        
    var THAT = this;
    
    this.set_order_catalog = function(open_order) {

        $rootScope.selected_order = open_order;

        THAT.products = [];

        angular.forEach(open_order.orderable_product_set, function(gsop) {

            var ordered_info = THAT.ordered_products_d[gsop.id];
            if (ordered_info === undefined) {
                ordered_info = { price : null, amount : 0, note : "" };
            }

            var el_prod = gsop.stock.product;
            var min_amount = parsingNumbers.parsing(gsop.stock.detail_minimum_amount);
            var step_unit = parsingNumbers.parsing(gsop.stock.detail_step);

            console.debug("Adding product " + el_prod.__unicode__ + " to open order "+ open_order.id+"...");

            THAT.products.push({
                id: gsop.id,
                category: el_prod.category,
                name: el_prod.__unicode__,
                price: gsop.stock.price,
                step: step_unit,
                min_amount: min_amount,
                quantity: ordered_info.amount,
                note: ordered_info.note
            });

            console.debug("done.");
        });
    };

    if (this.gm.open_orders.length > 0) {
        console.debug("Setting the default order catalog...");
        this.set_order_catalog(this.gm.open_orders[0]);
    } else {
        alert("Nessun ordine aperto per "+this.gm.gas.name);
    }

    this.increment = function(product) {
        if (product.quantity === 0) {
            product.quantity += product.min_amount;
            console.debug("Increment to min_amount for product " + product.name);
        } else {
            product.quantity += product.step;
            console.debug("Increment of "+ product.step + "=" + product.quantity + " for product " + product.name);
        }
    };

    this.change = function(product) {
        // Check if value is not under the minimum amount and
        // adjust the value if not in the right "tick" of min_amount + step
        if (product.quantity !== 0) {
            if (product.quantity < product.min_amount) {
                alert("La quantità minima per questo prodotto è "+ product.min_amount);
                product.quantity = product.min_amount;
            } else if ((product.quantity-product.min_amount)%product.step !== 0) {
                var base = product.quantity-product.min_amount;
                var next = parseInt(base/product.step, 10)*product.step+product.step;
                alert("Puoi ordinare " + next-product.step + " o " + next + " " + product.name + " ma non " + product.quantity);

                product.quantity = product.next;
            }
        }
    };

    this.decrement = function(product) {
        if (product.quantity === product.min_amount || product.quantity === 0) {
            product.quantity = 0;
        } else if (product.quantity === 0) {
            product.quantity = 0;
        } else {
            product.quantity -= product.step;
        }
    };

    this.getTotal = function() {
        var total = 0, i;
        for(i = 0; i < THAT.products.length; i++) {
            var product = THAT.products[i];
            total += (product.price * product.quantity);
        }
        return parseFloat(total).toFixed(2);
    };

    this.submitData = function() {
      
        var products_post = [];

        angular.forEach(THAT.products, function(product, i) {

            //FORMATTING products for the POST
            products_post.push({
                id: "",
                gsop_id: product.id,
                ordered_price: product.price,
                ordered_amount: product.quantity,
                note: product.note
            });
        });

        products_post.push({
            "form-TOTAL_FORMS": products_post.length,
            "form-INITIAL_FORMS": 0,
            "form-MAX_NUM_FORMS": ""
        });
        
        var POST_order_path = $.absurl_pre+'rest/gasmember/'+$routeParams.gm_id+'/order/edit_multiple';
        $http.post(POST_order_path, { form: products_post })
            .success(function(){
                alert("Prodotti aggiunti al paniere con successo!");
            })
            .error(function(){
                alert("C'è stato qualche problema, riprova");
            });
    };
});


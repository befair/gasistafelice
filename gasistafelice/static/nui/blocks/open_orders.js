
jQuery.UIBlockOO = jQuery.UIBlockWithList.extend({


    rendering_table_post_load_handler: function() {
        //$('id_datetime_end_0').css( 'color', 'red' );
        this._super();
    },

    //------------------------------------------------------------------------------//
    //                                                                              //
    //------------------------------------------------------------------------------//


})


jQuery.BLOCKS["open_orders"] = new jQuery.UIBlockOO("open_orders", "list");

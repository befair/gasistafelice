
jQuery.UIBlockBasketList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("basket", "table");
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    null,
                    null,
                    null,
                    null,
                    { "sType": "currency" }
                ]
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["basket"] = new jQuery.UIBlockBasketList();


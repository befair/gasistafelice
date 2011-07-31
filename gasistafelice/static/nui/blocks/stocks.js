
jQuery.UIBlockStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("stocks", "table");
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var ajaxSource = this.url + this.active_view;
        
        this.block_el.find('.dataTable').each(function() { $(this).dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": ajaxSource,
                "aoColumns": [
                    null,
                    null,
                    null,
                    { "sType": "currency" },
                    null
                ]
            }); 
        });
    },
    
});

jQuery.BLOCKS["stocks"] = new jQuery.UIBlockStockList();



jQuery.UIBlockGASStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("gasstocks", "table");
        this.active_view = "edit_multiple";
        this.default_view = this.active_view;
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
                    { "sType": "currency" },
                    null,
                    null,
                    null
                ]
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["gasstocks"] = new jQuery.UIBlockGASStockList();


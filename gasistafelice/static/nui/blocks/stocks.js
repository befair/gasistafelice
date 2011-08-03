
jQuery.UIBlockStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("stocks", "table");
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var ajaxSource = this.url + this.active_view;
        
        var oTable = this.block_el.find('.dataTable').dataTable({
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

        if (this.active_view = "edit_multiple") {
            $('#' + this.block_box_id + '-form').submit( function() {
                var sData = $(this).serialize();
                alert( "The following data would have been submitted to the server: \n\n"+sData );
                this.active_view = "view";
                return false;
            });
       }

    }
    
});

jQuery.BLOCKS["stocks"] = new jQuery.UIBlockStockList();


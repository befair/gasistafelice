
jQuery.UIBlockOrderReport = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("order_report", "table");
    },

    action_handler : function(action_el) {
        if (action_el.attr('name') == 'createpdf') {
            window.location = action_el.attr('url');
        } else {
            return this._super(action_el);
        }
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
                    { "sType": "currency" },
                    { "bSortable": "false" },
                    { "bSortable": "false" },
                    { "bSortable": "false", "sType": "currency" },
                ]
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["order_report"] = new jQuery.UIBlockOrderReport();



jQuery.UIBlockOrderReport = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("order", "table");
        this.active_view = "edit_multiple";
        this.default_view = this.active_view;
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
                'bPaginate': false, 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.dataSource + "?render_as=table",
                "aaSorting": [[5,"dsc"]],
                "aoColumns": [
                    null,
                    null,
                    { "bSortable": "false" },
                    { "bSortable": "false" },
                    { "bSortable": "false", "sType": "currency" },
                    { "bSortable": "false" },
                    { "sType": "currency" },
                ]
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["order"] = new jQuery.UIBlockOrderReport();


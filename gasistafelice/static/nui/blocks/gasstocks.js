
jQuery.UIBlockGASStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("gasstocks", "table");
        this.active_view = "edit_multiple";
        this.default_view = this.active_view;
    },

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"sWidth": "5%", "bSortable": false,},
                    null,
                    null,
                    { "sType": "currency" },
                    null,
                    null
                ],
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
                    /* Modify Django management form info */
                    /* FIXME TODO AFTER 6 UGLY !!!*/
                    $('#' + block_obj.block_box_id + '-form-TOTAL_FORMS').val(iEnd-iStart);
                }
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["gasstocks"] = new jQuery.UIBlockGASStockList();


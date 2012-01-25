
jQuery.UIBlockUserList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("users", "table");
        this.submit_name = "Attivazione utenti";
    },
//        this.active_view = "edit_multiple";
//        this.default_view = this.active_view;


//    action_handler : function(action_el) {
//        if (action_el.attr('name') == 'createpdf') {
//            window.location = action_el.attr('url');
//        } else {
//            return this._super(action_el);
//        }
//    },

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                'bLengthChange': true,
                "iDisplayLength": 150,
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"40%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"40%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%"},
                ],
                "oLanguage": {
                    "sLengthMenu": gettext("Display _MENU_ records per page"),
                    "sZeroRecords": gettext("Nothing found"),
                    "sInfo": gettext("Showing _START_ to _END_ of _TOTAL_ records"),
                    "sInfoEmpty": gettext("Showing 0 to 0 of 0 records"),
                    "sInfoFiltered": gettext("(filtered from _MAX_ total records)")
                },
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
                    /* Modify Django management form info */
                    /* FIXME TODO AFTER 6 UGLY !!!*/
                    $('#' + block_obj.block_box_id + '-form-TOTAL_FORMS').val(iEnd-iStart);
                }
            }); 

        return this._super();

    }

});

jQuery.BLOCKS["users"] = new jQuery.UIBlockUserList();


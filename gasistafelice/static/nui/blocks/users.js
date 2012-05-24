
jQuery.UIBlockUserList = jQuery.UIBlockWithList.extend({

    init: function(block_name) {
        this._super(block_name, "table");
        this.submit_name = "Attivazione utenti";
    },
//        this.active_view = "edit_multiple";
//        this.default_view = this.active_view;


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
                    {"bSearchable":true,"bSortable":true,"sWidth":"4%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"20%"},
                    {"bSearchable":false,"bSortable":true,"sWidth":"17%"},
                    {"bSearchable":false,"bSortable":true,"sWidth":"17%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%"}
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

//jQuery.BLOCKS["users"] = new jQuery.UIBlockUserList();
jQuery.BLOCKS["gas_users"] = new jQuery.UIBlockUserList("gas_users");
jQuery.BLOCKS["users"] = new jQuery.UIBlockUserList("supplier_users");



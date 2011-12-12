
jQuery.UIBlockFee = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("fee", "table");
        this.submit_name = "GAS membri: pagamento quota annuale del gassista";
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        // Init dataTables
//                'bPaginate': false,
        var iTot = 2;
        var block_obj = this;
        var oTable = this.block_el.find('.dataTable').dataTable({
                "bServerSide": true,
                "bStateSave": true,
                'sPaginationType': 'full_numbers',
                "iDisplayLength": 50,
                "aaSorting": [[1,'asc'], [0,'asc']],
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    { "sWidth": "10%", "bSortable" : true, "bSearchable" : true},
                    { "sWidth": "30%", "bSortable" : true, "bSearchable" : true},
                    { "sWidth": "40%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "10%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "10%", "bSortable" : false, "bSearchable" : false},
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

jQuery.BLOCKS["fee"] = new jQuery.UIBlockFee();


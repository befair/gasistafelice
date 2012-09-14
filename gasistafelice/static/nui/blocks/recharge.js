
jQuery.UIBlockRecharge = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("recharge", "table");
        this.submit_name = "Prepagato: ricarica il conto gasista";
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        // Init dataTables
//                'bPaginate': false,
//                "aaSorting": [[1,'asc'], [0,'asc']],
        var iTot = 2;
        var block_obj = this;
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers',
                'bLengthChange': true,
                "iDisplayLength": 50,
                "aaSorting": [[2,'asc']],
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    { "sWidth": "10%", "bSortable" : true, "bSearchable" : true},
                    { "sWidth": "25%", "bSortable" : true, "bSearchable" : true},
                    { "sWidth": "35%", "bSortable" : false, "bSearchable" : false, "sClass": "taright"},
                    { "sWidth": "10%", "bSortable" : false, "bSearchable" : false
                        , "sClass": "taright"
                    },
                    { "sWidth": "20%", "bSortable" : false, "bSearchable" : true
                        , "sClass": "taright"
                    },
                ],
                "oLanguage": {
                    "sLengthMenu": gettext("Display _MENU_ records per page"),
                    "sZeroRecords": gettext("Nothing found"),
                    "sInfo": gettext("Showing _START_ to _END_ of _TOTAL_ records"),
                    "sInfoEmpty": gettext("Showing 0 to 0 of 0 records"),
                    "sInfoFiltered": gettext("(filtered from _MAX_ total records)")
                },
                "fnRowCallback": function(nRow, aaData, iDisplayIndex, iDisplayIndexFull) {
                    try {
                        var url = aaData[5];
                        if (url != undefined) {
                            var _name = aaData[1];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[1]).html( res.render() );
                        }
                    }
                    catch(e){alert(e.message);
                    }
                    return nRow
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

jQuery.BLOCKS["recharge"] = new jQuery.UIBlockRecharge();


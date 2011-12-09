
jQuery.UIBlockStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("stocks", "table");
    },

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables
//                    {"bSearchable":true,"bSortable":true,"sWidth":"40%","bVisible":true},
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%","bVisible":true},
                    {"bSearchable":true,"bSortable":true,"sWidth":"50%","bVisible":true},
                   {"bSearchable":true, "bSortable":true, "sWidth":"20%", "sType":"currency","sClass": "taright" },
                    {"bSearchable":true,"bSortable":true,"sWidth":"20%",},
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
                        var url = aaData[4];
                        if (url != undefined) {
                            var _name = aaData[1];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[1]).html( res.render() );
                        }
                    }
                    catch(e){alert(e.message);
                    }
                    return nRow
                } ,
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
                    /* Modify Django management form info */
                    /* FIXME TODO AFTER 6 UGLY !!!*/
                    $('#' + block_obj.block_box_id + '-form-TOTAL_FORMS').val(iEnd-iStart);
                }
            }); 

        return this._super();

    }

});

jQuery.BLOCKS["stocks"] = new jQuery.UIBlockStockList();


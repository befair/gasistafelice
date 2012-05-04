
jQuery.UIBlockGASStockList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("gasstocks", "table");
        this.submit_name = "Aggiorna il listino GAS del produttore (sottoinsieme del listino DES)";
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers',
                'bLengthChange': true,
                "iDisplayLength": 50,
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%","bVisible": true},
                    {"bSearchable":true,"bSortable":true,"sWidth":"30%","bVisible": true},
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%","bVisible": true},
                    {"bSearchable":true,"bSortable":true,"sWidth":"15%", "sType": "currency", "sClass": "taright" },
                    {"bSearchable":false,"bSortable":true,"sWidth":"10%",},
                    {"bSearchable":false,"bSortable":true,"sWidth":"10%",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"10%","sClass":"taright",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"10%","sClass":"taright",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"10%","sClass":"taright",},
                ],
                "fnRowCallback": function(nRow, aaData, iDisplayIndex, iDisplayIndexFull) {
                    try {
                        var url = aaData[9];
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

jQuery.BLOCKS["gasstocks"] = new jQuery.UIBlockGASStockList();


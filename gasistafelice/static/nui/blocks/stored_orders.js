
jQuery.UIBlockOrdersStoredList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("stored_orders", "table");
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables

//        0: 'pk',
//        1: 'order',
//        2: 'tot_amount',
//        3: 'tot_gasmembers',
//        4: 'tot_price',
//        5: 'Invoice',
//        6: 'tot_curtail',
//        7: 'Payment'

//TODO Payment urn
        var iUrn = 8;
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%","bVisible": true},
                    {"bSearchable":false,"bSortable":false,"sWidth":"45%","bVisible": true},
                    {"bSearchable":false,"bSortable":false,"sWidth":"5%", "sType": "currency", "sClass": "taright" },
                    {"bSearchable":false,"bSortable":false,"sWidth":"5%"},

                    {"bSearchable":false,"bSortable":false,"sWidth":"5%", "sType": "currency", "sClass": "taright","sClass":"taright"},

                    {"bSearchable":false,"bSortable":false,"sWidth":"5%", "sType": "currency", "sClass": "taright","sClass":"taright"},
                    {"bSearchable":false,"bSortable":false,"sWidth":"5%", "sType": "currency", "sClass": "taright","sClass":"taright"},
                    {"bSearchable":false,"bSortable":false,"sWidth":"25%", "sType": "currency", "sClass": "taright","sClass":"taright"}
                ],
                "fnRowCallback": function(nRow, aaData, iDisplayIndex, iDisplayIndexFull) {
                    try {
                        var url = aaData[iUrn];
                        if (url != undefined) {
                            var _name = aaData[1];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[1]).html( res.render() );
                        }
                    }
                    catch(e){alert(e.message);
                    }
                    return nRow
                }
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["stored_orders"] = new jQuery.UIBlockOrdersStoredList();



//jQuery.BLOCKS["prepared_orders"] = new jQuery.UIBlockWithList("prepared_orders", "list");

jQuery.UIBlockOrdersPreparedList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("prepared_orders", "table");
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables

//        0: 'order', 'pk'
//        1: 'producer',
//        2: 'datetime_start',
//        3: 'referrer_person',
//        4: 'datetime_end'
//        5: 'group_id',
//        6: 'root_plan',


        var iUrn = 6
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%","bVisible": true},
                    {"bSearchable":true,"bSortable":true,"sWidth":"15%"},
                    {"bSearchable":false,"bSortable":true,"sWidth":"15%",},
                    {"bSearchable":true,"bSortable":true,"sWidth":"20%",},
                    {"bSearchable":false,"bSortable":true,"sWidth":"15%"},
                    {"bSearchable":false,"bSortable":true,"sWidth":"5%", "sClass": "tacenter"},
                    {"bSearchable":false,"bSortable":true,"sWidth":"10%"}
                ],
                "fnRowCallback": function(nRow, aaData, iDisplayIndex, iDisplayIndexFull) {
                    try {
                        var url = aaData[iUrn + 1];
                        if (url != undefined) {
                            var _name = aaData[0];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[0]).html( res.render() );
                        }
                        url = aaData[iUrn + 2];
                        if (url != undefined) {
                            var _name = aaData[1];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[1]).html( res.render() );
                        }
                        url = aaData[iUrn + 3];
                        if (url != undefined) {
                            var _name = aaData[3];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[3]).html( res.render() );
                        }
                        url = aaData[iUrn + 4];
                        if (url != undefined && url != "") {
                            var _name = aaData[6];
                            res = new jQuery.Resource(url, "Ord. " + _name);
                            $(nRow.cells[6]).html( res.render() );
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

jQuery.BLOCKS["prepared_orders"] = new jQuery.UIBlockOrdersPreparedList();


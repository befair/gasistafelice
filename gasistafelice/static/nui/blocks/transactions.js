
jQuery.UIBlockAccTransactsList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("transactions", "table");
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        // Init dataTables

//        0: 'pk',
//        1: 'date',
//        2: 'issuer',
//        3: 'source',
//        4: 'kind',
//        5: 'description',
//        6: 'is_confirmed'

        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers',
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%","bVisible": true},
                    {"bSearchable":false,"bSortable":false,"sWidth":"15%",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"15%",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"15%"},
                    {"bSearchable":false,"bSortable":false,"sWidth":"10%", "sClass":"taright"},
                    {"bSearchable":false,"bSortable":false,"sWidth":"30%"},
                ],
                "fnRowCallback": function(nRow, aaData, iDisplayIndex, iDisplayIndexFull) {
                    try {
                        var account_name = aaData[2]
                        var url_name = account_name.split("|");
                        if ((url_name != undefined) && (url_name.length >= 2)) {
                            var _name = url_name[0];
                            var _url = url_name[1];
                            res = new jQuery.Resource(_url, _name);
                            $(nRow.cells[2]).html( res.render() );
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

jQuery.BLOCKS["transactions"] = new jQuery.UIBlockAccTransactsList();

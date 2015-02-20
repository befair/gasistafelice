
jQuery.UIBlockAccTransactsList = jQuery.UIBlockWithList.extend({

    init: function(block_name) {
        this._super(block_name, "table");
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

//  $(document).ready(function() {
//    //alert('gfCP_from: ' +  $("#gfCP_from"));
//    $("#gfCP_from").datepicker();
//  });

        var block_obj = this;
        // Init dataTables

//        0: 'pk',
//        1: 'date',
//        2: 'issuer',
//        3: 'source',
//        4: 'kind',
//        5: 'description',
//        6: 'is_confirmed'

//                "aaSorting": [[1,'desc'], [0,'desc']],

        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers',
                'bLengthChange': true,
                "iDisplayLength": 50,
                "aaSorting": [[1,'desc']],
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true,"sWidth":"5%","bVisible": true},
                    {"bSearchable":false,"bSortable":true,"sWidth":"15%",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"10%",},
                    {"bSearchable":false,"bSortable":false,"sWidth":"10%"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"10%", "sClass":"taright"},
                    {"bSearchable":true,"bSortable":true,"sWidth":"40%"},
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

jQuery.BLOCKS["transactions"] = new jQuery.UIBlockAccTransactsList("transactions");
jQuery.BLOCKS["site_transactions"] = new jQuery.UIBlockAccTransactsList("site_transactions");
jQuery.BLOCKS["gasmember_transactions"] = new jQuery.UIBlockAccTransactsList("gasmember_transactions");

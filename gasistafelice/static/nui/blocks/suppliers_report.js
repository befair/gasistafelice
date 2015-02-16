
jQuery.UIBlockSupplierReport = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("suppliers_report", "table");
    },
        //this.submit_name = "Togli prodotti dall'ordine (elimina ordine gasista)";
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        // Init dataTables

//        0: 'pk', 
//        1: 'name',
//        2: 'frontman',
//        3: 'city',
//        4: 'mail',
//        5: 'phone',
//        6: 'tot_products',
//        7: 'tot_pacts',
//        8: 'balance',
//        9: 'certifications_list'

        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    { "sWidth": "5%"},
                    { "sWidth": "15%"},
                    { "sWidth": "15%"},
                    { "sWidth": "10%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "10%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "10%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "5%", "bSortable" : false, "sClass": "taright", "bSearchable" : false},
                    { "sWidth": "5%", "bSortable" : false, "sClass": "taright", "bSearchable" : false},
                    { "sWidth": "10%", "bSortable" : false, "sClass": "taright", "bSearchable" : false},
                    { "sWidth": "15%","bSearchable" : false}
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
                        var url = aaData[10];
                        if (url != undefined) {
                            var _name = aaData[1];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[1]).html( res.render() );
                        }
                    }
                    catch(e){alert(e.message);
                    }

                    return nRow;
                }
            });


        return this._super();

    }

});

jQuery.BLOCKS["suppliers_report"] = new jQuery.UIBlockSupplierReport();


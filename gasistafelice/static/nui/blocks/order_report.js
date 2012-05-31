
jQuery.UIBlockOrderReport = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("order_report", "table");
        this.submit_name = "Togli prodotti dall'ordine (elimina ordine gasista)";
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    action_handler : function(action_el) {
        if (action_el.attr('name') == 'createpdf') {
            window.location = action_el.attr('url');
        } else {
            return this._super(action_el);
        }
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var iTot = 7;
        var oTable = this.block_el.find('.dataTable').dataTable({
                'sPaginationType': 'full_numbers', 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    { "sWidth": "5%"},
                    { "sWidth": "30%"},
                    { "sWidth": "10%", "sType": "currency", "sClass": "taright", "bSearchable" : false},
                    { "sWidth": "5%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "10%", "bSortable" : false, "sClass": "taright", "bSearchable" : false},
                    { "sWidth": "5%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "15%", "bSortable" : false, "sClass": "taright", "bSearchable" : false},
                    { "sWidth": "15%", "bSortable" : false, "sClass": "taright", "bSearchable" : false},
                    { "sWidth": "5%"}
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
                        var url = aaData[9];
                        if (url !== undefined) {
                            var _name = aaData[1];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[1]).html( res.render() );
                        }
                    }
                    catch(e){alert(e.message);
                    }
                    return nRow;
                } ,
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {

                    var iTotal = 0;
                    var i=0;
                    for ( i=0; i<aaData.length; i++ ) {
                        iTotal += parseFloat(aaData[i][iTot].substr(8).replace(',','.'));
                    }

                    /* Modify the footer row to match what we want */
                    var nCells = $(nRow).find('th');
                    $(nCells[1]).html('&#8364; ' + String(GetRoundedFloat(iTotal)).replace('.',','));
                }
            });


        return this._super();

    }

});

jQuery.BLOCKS.order_report = new jQuery.UIBlockOrderReport();



jQuery.UIBlockBasketSentList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("basket_sent", "table");
    },

    action_handler : function(action_el) {
        if (action_el.attr('name') == 'createpdf') {
            window.location = action_el.attr('url');
        } else {
            return this._super(action_el);
        }
    },

    rendering_table_post_load_handler: function() {

        // Init dataTables
        var block_obj = this;
        var iQta = 5;
        var oTable = this.block_el.find('.dataTable').dataTable({
                'bPaginate': false,
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aaSorting": [[2,"asc"]],
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true, "sWidth": "30%"},
                    {"bSearchable":false,"bSortable":true, "sWidth": "15%"},
                    {"bSearchable":false,"bSortable":true, "sWidth": "25%"},
                    { "sType": "currency", "sClass": "taright", "sWidth": "10%","bSearchable":false },
                    {"bSortable":false, "sClass": "taright", "sWidth": "10%","bSearchable":false},
                    { "sType": "currency","bSortable":false, "sClass": "taright", "sWidth": "10%","bSearchable":false },
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
                        var url = aaData[iQta+1];
                        if (url != undefined) {
                            var _name = aaData[0];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[0]).html( res.render() );
                        }
                        url = aaData[iQta+2];
                        if (url != undefined) {
                            var _name = aaData[1];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[1]).html( res.render() );
                        }
                        url = aaData[iQta+3];
                        if (url != undefined) {
                            var _name = aaData[2];
                            res = new jQuery.Resource(url, _name);
                            $(nRow.cells[2]).html( res.render() );
                        }
                    }
                    catch(e){//alert(e.message);
                    }
                    return nRow
                },
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
                    var iTotal = 0;
                    for ( var i=0 ; i<aaData.length ; i++ )
                    {
                        iTotal += parseFloat(aaData[i][iQta].substr(8).replace(',','.'));
                    }
                    
                    /* Modify the footer row to match what we want */
                    var nCells = $(nRow).find('th');
                    $(nCells[1]).html('&#8364; ' + String(GetRoundedFloat(iTotal)).replace('.',','));

                    /* Modify Django management form info */
                    /* FIXME TODO AFTER 6 UGLY !!!*/
                    $('#' + block_obj.block_box_id + '-form-TOTAL_FORMS').val(iEnd-iStart);

                }
            });

        return this._super();

    }

});

jQuery.BLOCKS["basket_sent"] = new jQuery.UIBlockBasketSentList();


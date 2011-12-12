
jQuery.UIBlockOrderReport = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("curtail", "table");
        this.submit_name = "Decurta conto gassista per un dato ordine";
    },
        //this.active_view = "edit_multiple";
        //this.default_view = this.active_view;

    rendering_table_post_load_handler: function() {

        // Init dataTables
//                'sPaginationType': 'full_numbers', 
        var iTot = 2;
        var block_obj = this;
        var oTable = this.block_el.find('.dataTable').dataTable({
                'bPaginate': false,
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aoColumns": [
                    { "sWidth": "10%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "50%", "bSortable" : false, "bSearchable" : false},
                    { "sWidth": "20%", "bSortable" : false, "bSearchable" : false, "sClass": "taright"},
                    { "sWidth": "20%", "bSortable" : false, "bSearchable" : false
                        , "sClass": "input_payment taright"
                    },
                ],
                "oLanguage": {
                    "sLengthMenu": gettext("Display _MENU_ records per page"),
                    "sZeroRecords": gettext("Nothing found"),
                    "sInfo": gettext("Showing _START_ to _END_ of _TOTAL_ records"),
                    "sInfoEmpty": gettext("Showing 0 to 0 of 0 records"),
                    "sInfoFiltered": gettext("(filtered from _MAX_ total records)")
                },
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {

                    var iOrdered = 0;
                    var iTotal = 0;
                    var tmp = '';
                    var idstr = 'text'
                    for ( var i=0 ; i<aaData.length ; i++ )
                    {
                        iTotal += parseFloat(aaData[i][iTot].substr(8).replace(',','.'));
                        tmp = aaData[i][iTot+1].replace(',','.')
                        if (tmp != '') {
                            if (tmp.indexOf(idstr) > 0) {
                                tmp = tmp.slice(tmp.lastIndexOf(idstr))
                                tmp = tmp.slice(tmp.indexOf('value="'))
                                tmp = tmp.slice(tmp.indexOf('"') + 1)
                                tmp = tmp.substr(0, tmp.indexOf('"'))
                                tmp = tmp.replace(',','.')
                                //el = $(nRow.cells[3]).next('input') tmp = el.val();
                            }
                            iOrdered += parseFloat(tmp);
                        }
                    }

                    /* Modify the footer row to match what we want */
                    var nCells = $(nRow).find('th');
                    $(nCells[1]).html('&#8364; ' + String(GetRoundedFloat(iTotal)).replace('.',','));
                    $(nCells[2]).html('&#8364; ' + String(GetRoundedFloat(iOrdered)).replace('.',','));

                    if (iTotal != iOrdered) {
                        sinit1 = '<font color="#green">   '
                        sinit2 = '<font color="#red">   '
                        if (iTotal > iOrdered)
                            sinit = sinit1;
                        else
                            sinit = sinit2;
                        send = '</font>'
                        tmp = $(nCells[0]).html();
                        if (tmp.indexOf(sinit1) > 0) 
                            tmp = tmp.substr(0, tmp.indexOf(sinit1))
                        else if (tmp.indexOf(sinit2) > 0) 
                            tmp = tmp.substr(0, tmp.indexOf(sinit2))
                        $(nCells[0]).html(tmp + sinit + ' Diff. &#8364; ' + String(GetRoundedFloat(iTotal - iOrdered)).replace('.',',') + send);
                    }
                    /* Modify Django management form info */
                    /* FIXME TODO AFTER 6 UGLY !!!*/
                    $('#' + block_obj.block_box_id + '-form-TOTAL_FORMS').val(iEnd-iStart);
                }
            });

//        "{{row.ordered_product__order|escapejs}}",
//        "{{row.purchaser|escapejs}}",
//        "{{row.tot_product}}",
//        "{{row.sum_qta}}",
//        "{{row.sum_price}}",
//        "&#8364; {{row.sum_amount|floatformat:"2"}}",
//        "{{row.amounted|escapejs}}",

        return this._super();

    }

});

jQuery.BLOCKS["curtail"] = new jQuery.UIBlockOrderReport();


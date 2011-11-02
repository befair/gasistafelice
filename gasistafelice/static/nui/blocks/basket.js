
jQuery.UIBlockBasketList = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("basket", "table");
        this.active_view = "edit_multiple";
        this.default_view = this.active_view;
        this.submit_name = "Aggiorna il tuo paniere";
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
        var iQta = 6;
        var oTable = this.block_el.find('.dataTable').dataTable({
                'bPaginate': false,
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aaSorting": [[2,"asc"]],
                "aoColumns": [
                    {"bSearchable":true,"bSortable":true, "sWidth": "5%"},
                    {"bSearchable":true,"bSortable":true, "sWidth": "5%"},
                    {"bSearchable":false,"bSortable":true, "sWidth": "20%",
                      "fnRender": function ( oObj ) {
                                    var url = $(oObj.aData[iQta]).attr('s_url');
                                    var _name = oObj.aData[ oObj.iDataColumn ];
                                    res = new jQuery.Resource(url, _name);
                                    return res.render();
                                  },
                    },
                    {"bSearchable":false,"bSortable":true, "sWidth": "30%",
                      "fnRender": function ( oObj ) {
                                    var url = $(oObj.aData[iQta]).attr('p_url');
                                    var _name = oObj.aData[ oObj.iDataColumn ];
                                    res = new jQuery.Resource(url, _name);
                                    return res.render();
                                  },
                    },
                    { "sType": "currency", "sClass": "taright", "sWidth": "10%","bSearchable":false },
                    {"sWidth": "5%","bSearchable":false,"bSortable":false},
                    {"bSortable":false, "sClass": "taright", "sWidth": "15%","bSearchable":false, 
                      "fnRender": function ( oObj ) {
                                    var step = $(oObj.aData[iQta]).attr('step');
                                    var min =  $(oObj.aData[iQta]).attr('minimum_amount');
                                    var price =  parseFloat(oObj.aData[iQta-2].replace(',','.').replace('&#8364;',''));
                                    var rv = '<span class="hand" onclick="fncOrder($(this),-'+ step +','+ min + ', ' + price + '); return false;"><img src="/static/nui/img/remove.png"></span>'; 
                                    rv += oObj.aData[iQta];
                                    rv += '<span class="hand" onclick="fncOrder($(this),+'+ step +','+ min + ', ' + price + '); return false;"><img src="/static/nui/img/add.png"></span>';
                                    return rv
                                  },
                     },
                    { "sType": "currency","bSortable":false, "sClass": "taright", "sWidth": "10%","bSearchable":false },
                    {"sWidth": "5%","bSearchable":false,"bSortable":false},
                    {"sWidth": "5%","bSearchable":false,"bSortable":false},
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
                        var priceStatus = $($(aaData[iQta])[1]).attr('eur_chan');
                        var confirmStatus = $($(aaData[iQta])[1]).attr('req_conf');
                        //alert("["+ iQta + "]Price has changed: " + priceStatus + ", is confirmed: " + confirmStatus)
                        $(nRow).addClass(confirmStatus);
                        $(nRow.cells[4]).addClass(priceStatus);
                        $(nRow.cells[8]).addClass(priceStatus);
                        $(nRow.cells[9]).addClass(confirmStatus);
                    }
                    catch(e){alert(e.message);
                    }
                    return nRow
                } ,

                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
                    var iTotal = 0;
                    for ( var i=0 ; i<aaData.length ; i++ )
                    {
                        iTotal += parseFloat(aaData[i][iQta+1].substr(8).replace(',','.'));
                    }
                    
                    /* Modify the footer row to match what we want */
                    var nCells = $(nRow).find('th');
                    $(nCells[1]).html('&#8364; ' + String(GetRoundedFloat(iTotal)).replace('.',','));

                }
            });

        return this._super();

    }

});

jQuery.BLOCKS["basket"] = new jQuery.UIBlockBasketList();


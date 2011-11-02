
jQuery.UIBlockOrderReport = jQuery.UIBlockWithList.extend({

    init: function() {
        this._super("order", "table");
        this.active_view = "edit_multiple";
        this.default_view = this.active_view;
        this.submit_name = "Metti nel paniere";
    },

    action_handler : function(action_el) {
        if (action_el.attr('name') == 'createpdf') {
            window.location = action_el.attr('url');
        } else {
            return this._super(action_el);
        }
    },

    rendering_table_post_load_handler: function() {

        var block_obj = this;
        var iQta = 5;
        // Init dataTables
                //'bPaginate': false, 'sPaginationType': 'full_numbers', 
                //"oColVis": {"aiExclude": [ 0 ]},
        var oTable = this.block_el.find('.dataTable').dataTable({
                'bPaginate': false,
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.get_data_source(),
                "aaSorting": [[1,"asc"]],
                "aoColumns": [
                    {"bSearchable":true, "sWidth": "4%", "bVisible": true },
                    {"bSearchable":true,"bSortable":true, "sWidth": "16%",
                      "fnRender": function ( oObj ) {
                                    var url = $(oObj.aData[iQta]).attr('s_url');
                                    var _name = oObj.aData[ oObj.iDataColumn ];
                                    res = new jQuery.Resource(url, _name);
                                    return res.render();
                                  },
                    },
                    {"bSortable":true,"bSearchable":true, "sWidth": "25%",
                      "fnRender": function ( oObj ) {
                                    var url = $(oObj.aData[iQta]).attr('p_url');
                                    var _name = oObj.aData[ oObj.iDataColumn ];
                                    res = new jQuery.Resource(url, _name);
                                    return res.render();
                                  },
                    },
                    {"bSortable":false,"bSearchable":false, "sWidth": "20%"},
                    {"bSortable":true, "sClass": "taright", "sType": "currency","bSearchable":false, "sWidth": "10%"},
                    {"bSortable":false,"bSearchable":false, "sWidth": "15%",
                      "fnRender": function ( oObj ) {
                                    var step = $(oObj.aData[iQta]).attr('step');
                                    var min =  $(oObj.aData[iQta]).attr('minimum_amount');
                                    var price =  parseFloat(oObj.aData[iQta-1].replace(',','.').replace('&#8364;',''));
                                    var rv = '<span class="hand" onclick="fncOrder($(this),-'+ step +','+ min + ', ' + price + '); return false;"><img src="/static/nui/img/remove.png"></span>'; 
                                    rv += oObj.aData[iQta];
                                    rv += '<span class="hand" onclick="fncOrder($(this),+'+ step +','+ min + ', ' + price + '); return false;"><img src="/static/nui/img/add.png"></span>';
                                    return rv
                                  },
                     },
                    {"bSortable":false, "sType": "currency","bSearchable":false, "sWidth": "10%" },
                ],
                "oLanguage": {
                    "sLengthMenu": gettext("Display _MENU_ records per page"),
                    "sZeroRecords": gettext("Nothing found"),
                    "sInfo": gettext("Showing _START_ to _END_ of _TOTAL_ records"),
                    "sInfoEmpty": gettext("Showing 0 to 0 of 0 records"),
                    "sInfoFiltered": gettext("(filtered from _MAX_ total records)")
                },
                "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {

                    var iTotal = 0;
                    for ( var i=0 ; i<aaData.length ; i++ )
                    {
                        iTotal += parseFloat(aaData[i][iQta+1].substr(8).replace(',','.'));
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

jQuery.BLOCKS["order"] = new jQuery.UIBlockOrderReport();



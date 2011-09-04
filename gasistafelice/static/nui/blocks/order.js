
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

        // Init dataTables
        var oTable = this.block_el.find('.dataTable').dataTable({
                'bPaginate': false, 
                "bServerSide": true,
                "bStateSave": true,
                "sAjaxSource": this.dataSource + "?render_as=table",
                "aaSorting": [[5,"dsc"]],
                "aoColumns": [
                    null,
                    null,
                    { "bSortable": "false" },
                    { "bSortable": "false" },
                    { "bSortable": "false", 
                      "sType": "currency",
                      "fnRender": function (oObj) {
                                    return '&#8364; ' + oObj.aData[4];
                                  },
                    },
                    { "bSortable": "false",
                      "fnRender": function ( oObj ) {
                                    var step = $(oObj.aData[5]).attr('step');
                                    var min =  $(oObj.aData[5]).attr('minimun_amount');
                                    var rv = '<a href="#" onclick="var el = $(this).next(\'input\'); \
                                                var n = parseInt(el.val()); n == ' + min + '? el.val(0) : n > ' + min +'? \
                                                el.val(n-' + step +'):0; return false"><img src="/static/nui/img/remove.png">\
                                             </a>'; 
                                    rv += oObj.aData[5]; 
                                    rv += '<a href="#" onclick="var el = $(this).prev(\'input\'); \
                                            var n = parseInt(el.val()); el.val(n+' + step +'); \
                                            var next_td = $(this).parent(\'td\').next(); \
                                            next_td.html(\'&#8364; \' + parseInt(el.val())*' + parseFloat(oObj.aData[4].substr(8).replace(',','.')) +'); \
                                            return false"><img src="/static/nui/img/add.png">\
                                          </a>';
                                    return rv
                                  },
                     },
                    { "sType": "currency" },
                ],
                "oLanguage": {
                    "sLengthMenu": gettext("Display _MENU_ records per page"),
                    "sZeroRecords": gettext("Nothing found"),
                    "sInfo": gettext("Showing _START_ to _END_ of _TOTAL_ records"),
                    "sInfoEmpty": gettext("Showing 0 to 0 of 0 records"),
                    "sInfoFiltered": gettext("(filtered from _MAX_ total records)")
                }
            }); 

        return this._super();

    }
    
});

jQuery.BLOCKS["order"] = new jQuery.UIBlockOrderReport();


//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.UIBlockOrderInvoice = jQuery.UIBlock.extend({

    action_handler : function(action_el) {
        if (action_el.attr('name') == "new_note") {
            return this.open_new_note_form(action_el.attr('url'));
        } else {
            return this._super(action_el);
        }
    },

    render_content : function(data) {

        function capitalize_str(s) {
            c = s.substring(0,1).toUpperCase();
            s = c + s.substring(1, s.length);
            return s;
        }
        
            
        //template elements
        var details_template = "\
        <div>\
            <form >\
            @@content@@\
            </form>\
        </div>\
        "

/*
            <table border='0' width='100%' > \n\
                <tr>\n\
                    <td valign='center' width='100%'>\n\
                        \n\
                        <table border='0'>\n\
                            <tr>\
                                <td colspan='2'>\
                                    <a class='ctx_enabled resource inline @@resource_type@@' href='#rest/@@resource_type@@/@@resource_id@@/'>@@resource_descr@@</a> \n\
                                </td>\
                            </tr>\
                            @@inforow@@\n\
                        </table>\n\
                    </td>\n\
                    <td valign='top' align='center'>\n\
                        <img style='margin:5px' src='@@img@@'>\n\
                    </td>\n\
                </tr>\n\
                <tr >\n\
                    <td colspan='2'>\n\
                        @@more_details@@\n\
                    </td>\n\
                </tr>\
            \n\
            </table>\n\
            </br>\n\
            <table border='0'> \n\
                <tr >\n\
                    <td>\n\
                        <table> \n\
                            @@notes_rows@@ \n\
                        </table> \n\
                    </td>\n\
                </tr>\n\
            </table>\n\
            \
        </div>";
        
*/        


        BLOCK_ELEMENT = jQuery.parseXml(data);

        //code
        jQel = jQuery(BLOCK_ELEMENT);
        
        if (jQel.children('error').length != 0)
            return jQel.text()
        
        var form_html = jQel.find('content[type="table"]').html();
            
        details_template = details_template.replace(/@@content@@/g, form_html);
        
        return details_template;
        
        //var b = jQel.find('block[type=details]');
        var sanet_urn     = jQel.attr('sanet_urn');
        var resource_type = jQel.attr('resource_type');
        var resource_id   = jQel.attr('resource_id');

        var descr         = capitalize_str( jQel.children('descr').text() );

        
        details_template = details_template.replace(/@@resource_type@@/g, resource_type);
        details_template = details_template.replace(/@@resource_id@@/g  , resource_id);
        details_template = details_template.replace(/@@sanet_urn@@/g    , sanet_urn);
        details_template = details_template.replace('@@resource_descr@@', descr);


        
        //
        // details
        //
        /*
        resource_element = "<li class='resource @@resource_type@@ @@resource_status@@'>					\n\
                    <a class='ctx_enabled' \
                       sanet_urn='@@sanet_urn@@' \
                       href='#rest/@@resource_type@@/@@resource_id@@/'>@@resource_descr@@</a> \n\
                    </li> \n\
                    ";
        */
        resource_element = "\
                    <a class='ctx_enabled resource @@resource_type@@ @@resource_status@@ inline' \
                       sanet_urn='@@sanet_urn@@' \
                       href='#rest/@@resource_type@@/@@resource_id@@/'>@@resource_descr@@</a> \
                    \
                    ";
        
        
        var infos = jQel.find('content[type="info"]');
        
        infos.find('info').each(function(){
            var text     = $(this).children('text').text();
            var val_obj  = $(this).children('value');
            var val_type = val_obj.attr('type');
            var val_warning = $(this).children('warning').text();
            var val = '-';
            
            if (val_type=='str') {
                if (val_warning=='on')
                    val = "<span style='color:red'>" + val_obj.text() + "</a>";
                else
                    val  = val_obj.text();
            } else if (val_type=='file') {
                val  = '<a href="' +val_obj.text() + '" > ' + val_obj.text() + '</a>';
            } else if (val_type=='email') {
                val  = '<a href="mailto:' +val_obj.text() + '" > ' + val_obj.text() + '</a>';
            } else if (val_type=='bool') {
                val = jQuery.render_bool(val_obj.text());
            } else if (val_type == 'resource') {
                
                var res = $(val_obj.children()[0]);
                res = new jQuery.Resource(res.attr('type')+'/'+res.attr('id'), res.text());
                var val = res.render();
                
            } else if (val_type == 'resourcelist') {
                
                var val = '';
                var html = '-';
                
                var first = 1;
                
                val_obj.find('resource').each( function (){
                    
                    if (html == '-')
                        html = '';
                        
                    var rid    = $(this).attr('id');
                    
                    if (rid != "") {
                        var rtype  = $(this).attr('type');
                        var status = $(this).attr('status');
                        var descr  = $(this).text();			
                        var urn   = rtype + "/" + rid;
                        
                        var e = '';
                        
                        if (first != 1)
                            e += ' ';
                        first = 0;
                        
                        e += resource_element;
                        
                        e = e.replace(/@@resource_type@@/g , rtype);
                        e = e.replace(/@@resource_id@@/g   , rid);
                        e = e.replace(/@@sanet_urn@@/g     , urn);
                        e = e.replace('@@resource_descr@@' , descr.trim());
                        e = e.replace('@@resource_status@@', status);
                        
                        html += e;
                    }
                    else {
                        html += '-';	
                    }
                });
                
                val = html;
                
            }

            var a = inforow.replace("@@text@@", capitalize_str(text));
                a = a.replace('@@val@@', val);
            
            
            details_template = details_template.replace('@@inforow@@', a);
        });
        details_template = details_template.replace('@@inforow@@', '');

        //
        // more details
        //
        var more_details = jQel.find('content[type="more_details"]');
        details_template = details_template.replace("@@more_details@@", more_details.text() )

        
        return details_template;
    },
	
    //------------------------------------------------------------------------------//
    //                                                                              //
    //------------------------------------------------------------------------------//


})

jQuery.BLOCKS["order_invoice"] = new jQuery.UIBlockOrderInvoice("order_invoice");


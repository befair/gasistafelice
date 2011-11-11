//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.UIBlockDetails = jQuery.UIBlock.extend({

    render_actions : function(data) {

        var list_actions = this._super(data);

        // Append "add note" action in rendered data
        
        var action_new_note_template = '<input type="button" value="' + gettext("Add note")+ '" href="#" url="@@new_note_action@@" class="block_action" name="new_note" popup_form="1" />';
        new_note_action = this.resource.absolute_url + "/details/new_note";

        action_new_note_template = action_new_note_template.replace('@@new_note_action@@', new_note_action);

        //TODO: ugly but I don't know how to do better now
        var res = $('<p> </p>');
        list_actions = $(list_actions).append(action_new_note_template);
        return res.append(list_actions).html();

    },

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
        
        var user_options_text = "\
            <div style='font-size: 0.8em;'>" + gettext("WARNING: some informations are omissed due to block's configuration") + ": <span style='color:red'>@@text@@ </span> </div> \
            ";
            
                
        //template elements
        var details_template = "\
        <div>\
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
            @@user_options@@\
            \
        </div>";
        
        
        var inforow = "\n\
            <tr>\n\
                <td width='30%'>@@text@@</td>\n\
                <td width='70%'>@@val@@</td>\n\
            </tr>\n\
            @@inforow@@";

        var note_row = "					\
            <tr  id='note_row_@@note_id@@'><td> 		\
                <span class='note_row'> 		\
                    <a onclick='return jQuery.remove_note(@@note_id@@)' \
                       href='@@delete_action@@'>	\
                       " + gettext("Remove") + "	\
                    </a> 				\
                    @@resource@@ \
                    - @@date@@ 			\
                    - @@author@@ 			\
                    - @@text@@ 			\
                </span> 				\
            </td></tr> 						\
            @@note_row@@";



        BLOCK_ELEMENT = jQuery.parseXml(data);

        //code
        jQel = jQuery(BLOCK_ELEMENT);
        
        if (jQel.children('error').length != 0)
            return jQel.text()
        
            
        
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
        //
        //	
        var img = jQel.find('content[type="image"]');
        var imgaddr = "";
        img.find('img').each(function(){
            imgaddr = $(this).attr('src');
        });
        details_template = details_template.replace("@@img@@", imgaddr)
        
        
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

        
        //
        // NOTES
        //
        
        var notes_rows = ''

        
        var notes = jQel.find('content[type="notes"]');
        notes.find('note').each(function(){
            
            if (notes_rows == '')
                notes_rows = note_row
            else
                notes_rows = notes_rows.replace('@@note_row@@', note_row);
            
            var note_id = $(this).attr('id');
            var date   = $(this).children('date').text();
            var author = $(this).children('author').text();
            var text   = $(this).children('text').text();
            
            var resource_text = ''
            var resource = $(this).children('resource');
            resource.each(function() {
                var sanet_urn = resource.attr('sanet_urn');
                var descr     = resource.text();

                var rtype     = sanet_urn.split('/')[0];
                var rid       = sanet_urn.split('/')[1];

                resource_text = "<span class='resource " + rtype + " inline '> <a class='ctx_enabled' href='#rest/"+sanet_urn+"' sanet_urn='"+sanet_urn+"'>" + descr + "</a> </span>";
            });
            notes_rows = notes_rows.replace("@@resource@@", resource_text);	
            
            
            
            
            //alert('nota' + note_id);

            var delete_action = jQuery.pre + "rest/" + sanet_urn + "/details/remove_note?note_id=" + note_id;	
            
            notes_rows = notes_rows.replace("@@date@@", date);
            notes_rows = notes_rows.replace(/@@note_id@@/g, note_id);
            notes_rows = notes_rows.replace("@@author@@", author);
            notes_rows = notes_rows.replace("@@text@@", text);
            notes_rows = notes_rows.replace("@@delete_action@@", delete_action);
            
            
        });
        notes_rows = notes_rows.replace('@@note_row@@', '');
        details_template = details_template.replace('@@notes_rows@@', notes_rows);
        
        //
        // Show informations about the user settings
        //
        
        var user_options = '';
        var infos = jQel.find('content[type=info]');
        if (infos.find('item').length > 0) {
            infos.find('item').each(function(){
                var param  = $(this).attr('name');
                var value  = $(this).text();
                
                if (param == 'max_num_problems' && value != '') 
                    user_options += '<b>DN</b>' + ' = ' + value + ', ';	
                else if (param == 'max_num_uncheckables' && value != '') 
                    user_options += '<b>UN</b>' + ' = ' + value + ', ';
            });	
        }
        
        if (user_options != '') 
            user_options_text = user_options_text.replace("@@text@@", user_options);
        else 
            user_options_text = ''
        details_template = details_template.replace('@@user_options@@', user_options_text);	
        
        return details_template;
    },
	
    //------------------------------------------------------------------------------//
    //                                                                              //
    //------------------------------------------------------------------------------//

    open_new_note_form : function (note_action) {
	
        var form_html = NEW_NOTE_FORM_TEXT.replace("@@new_note_action@@", note_action);
        
        //
        // Initialize dialog component
        //
        var block_instance = this;
        var options = { 
            success : function (responseText, statusText)  { 
                block_instance.update_handler(block_instance.block_box_id);
            }
        }		
	
        //
        // CREATE THE DIALOG
        //
        $(NEW_NOTE_DIALOG).dialog('close');
        $(NEW_NOTE_DIALOG).dialog('destroy');
        
        $(NEW_NOTE_DIALOG).empty();
        $(NEW_NOTE_DIALOG).append(form_html);
        
        var buttons = new Object();
        buttons[gettext('Confirm')] = function() {
            //
            // "hide"/close the dialog
            //
            $(NEW_NOTE_DIALOG).dialog('destroy');
            $(NEW_NOTE_DIALOG).dialog('close');
            $(NEW_NOTE_FORM).ajaxSubmit(options);
        };
        
        $(NEW_NOTE_DIALOG).dialog({
            title: gettext("New note"),
            bgiframe: true,
            autoOpen: false,
            width: 600,
            height: "auto",
            modal: true,
            buttons: buttons,
            close: function() { }
        });
        
        $(NEW_NOTE_DIALOG).dialog('open');
        
        return false;
        
    }

})

//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.remove_note = function(note_id) 
{	
	ask_confirm(
		gettext("Do you really want to delete this note?")  // "Sei sicuro di voler cancellare la nota?" 
		, function() { jQuery.remove_note2(note_id);  }
		, function() { }
	);	
	
	// block onclick() event
	return false;				
}

jQuery.remove_note2 = function(note_id) 
{	
	var delete_url = jQuery.pre + "rest/" + sanet_urn + "/details/remove_note?note_id=" + note_id;	

	// Send the GET command and delete the row identified by "report_row_id"
	// if the GET is successful.
	jQuery.get(delete_url, function (response_data) {

		if (response_data.match('class="success"')) {
			
			$('#note_row_'+note_id).remove();
		}
	});

	
	return false;
}


jQuery.BLOCKS["details"] = new jQuery.UIBlockDetails("details");

// FIXME
// Nest here other registering calls: this can be done without losing performance
// because blocks are not autorefreshing. This is a temporary solution to avoid
// trickeries like http://www.phpied.com/javascript-include/

//jQuery.BLOCKS["gas_details"] = new jQuery.UIBlockDetails("gas_details");
//jQuery.BLOCKS["pact_details"] = new jQuery.UIBlockDetails("pact_details");
//jQuery.BLOCKS["order_details"] = new jQuery.UIBlockDetails("order_details");
//jQuery.BLOCKS["stock_details"] = new jQuery.UIBlockDetails("stock_details");
//jQuery.BLOCKS["supplier_details"] = new jQuery.UIBlockDetails("supplier_details");
jQuery.BLOCKS["gasmember_details"] = new jQuery.UIBlockDetails("gasmember_details");

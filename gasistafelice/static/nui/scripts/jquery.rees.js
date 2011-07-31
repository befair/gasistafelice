
/* GLOBAL DEFINITIONS */

String.prototype.trim = function() { return this.replace(/(^\s+)/, '').replace(/(\s+$)/, ''); };

var NEW_NOTE_DIALOG = '#global_dialog_placeholder';

var NEW_NOTE_FORM   = '#new_note_form';

var NEW_NOTE_FORM_TEXT= "\
		<form name='new_note_form' id='new_note_form' method='post' action='@@new_note_action@@'>\
			" + gettext('Text') + ":  <br /> \
			<textarea id='' name='body'  cols='65' row='10' /> \
		</form>\
		";

/* BLOCK_REGISTER_DISPLAY and BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME 
   are meant to store representation of blocks

   * BLOCK_REGISTER_DISPLAY is like block_box_id => display_type
   * BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME is like block_name => display_type 
     (block_name are keys registered in settings.RESOURCE_PAGE_BLOCKS)
     This acts as default display_type for block_box_id display type
*/

jQuery.BLOCK_REGISTER_DISPLAY = {}
jQuery.BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME = {}

jQuery.render_actions = function (block_box_id, contents) {

    // Block actions
    var block_action_template = "<a href=\"@@action_url@@\" class=\"block_action\">@@action_verbose_name@@</a>";
    var block_actions = '';

	if (contents.find('action').length > 0) {
	
		contents.find('action').each(function(){
            var block_action = block_action_template.replace(/@@action_name@@/g, $(this).attr("name"));
            block_action = block_action.replace(/@@action_verbose_name@@/g, $(this).attr("verbose_name"));
            block_action = block_action.replace(/@@action_url@@/g, $(this).attr("url"));
            block_actions += block_action;
        });
    }
    return block_actions;
    
}

/* Display resource list */
/* This function is inspired by blocks specific code of SANET by Laboratori Guglielmo Marconi */
jQuery.resource_list = function (block_box_id, element) {

	var res = "		\
    <div class='list_actions'>@@list_actions@@</div> \
	<table> 		\
		@@inforow@@	\
	</table> 		\
	";
	
		
	var inforow = " \
		<tr id='@@row_id@@' > 			\
			<td width='100%'>   			\
				<span class='resource row' > \
					<a class='ctx_enabled resource inline @@resource_type@@' sanet_urn='@@urn@@' href='@@link@@'> @@name@@ </a> 			\
				</span> \
			</td>		     			\
			<td>		     			\
			@@actions@@ \
			</td>		     			\
		</tr>	 			\
		@@inforow@@ \
	";

	element = jQuery.parseXml(element);	
	
	//code
	var jQel = jQuery(element);
	
	if (jQel.children('error').length > 0)
		return jQel.text()
	
	// Resource ID
	var resource_type =  jQel.attr('resource_type');
	var resource_id   =  jQel.attr('resource_id');
	
    // Block content
	var contents = jQel.find('content[type="user_actions"]');

    res = res.replace('@@list_actions@@', jQuery.render_actions(block_box_id, contents));

    // Resources
	var contents = jQel.find('content[type="list"]');
	
	if (contents.find('info').length > 0) {
	
		contents.find('info').each(function(){
			
			var urn = $(this).attr('sanet_urn');
			var name = $(this).attr('name');
			var link = "#rest/"+urn;

			var row_id = resource_type + '_row_' + urn.split('/').join('_');

			var a = inforow
			
			a = a.replace(/@@resource_type@@/g, resource_type);
			a = a.replace(/@@row_id@@/g, row_id);
			a = a.replace(/@@name@@/g, name);
			a = a.replace(/@@urn@@/g,urn);
			a = a.replace(/@@link@@/g,link);
			
			var actions = ''

//TODO fero: row_actions
//			if (resource_type == 'usercontainer') {
//				actions = user_actions
//				
//				usercontainer_urn = resource_type + '/' + resource_id;
//				
//				actions = actions.replace(/@@usercontainer_urn@@/, usercontainer_urn);
//				actions = actions.replace(/@@node_urn@@/       , urn);
//				
//			}
			a = a.replace(/@@actions@@/g, actions);		

			res = res.replace('@@inforow@@', a);
		});
		
		res = res.replace('@@inforow@@', '');	
	}
	else {
		res = res.replace('@@inforow@@', gettext('There are no elements related to this resource.'));
	}

	return res;
}

/* Display resource list with details */
jQuery.resource_list_with_details = function (block_box_id, element) {

	var res = "		\
    <div class='list_actions'>@@list_actions@@</div> \
		@@table@@	\
	";
	
	element = jQuery.parseXml(element);	
	
	//code
	var jQel = jQuery(element);
	
	if (jQel.children('error').length > 0)
		return jQel.text()
	
	// Resource ID
	var resource_type =  jQel.attr('resource_type');
	var resource_id   =  jQel.attr('resource_id');
	
    // Block content
	var contents = jQel.find('content[type="user_actions"]');

    res = res.replace('@@list_actions@@', jQuery.render_actions(block_box_id, contents));

    // Resources
	var contents = jQel.find('content[type="table"]');
	
    res = res.replace('@@table@@', contents.html());
	return res;
}

/* Display resource list as icons */
jQuery.resource_list_as_icons = function (block_box_id, element) {
    /* TODO */
}

/* Retrieve and update blocks that include resource list */
jQuery.resource_list_block_update = function(block_box_id) {

	var block_box_el = $('#' + block_box_id);
	var block_el  = block_box_el.children('.block_body');
	
	block_el.empty();
	
	var block_urn = block_box_el.attr('block_urn');
	var block_name = block_box_el.attr('block_name');
	
	var url = jQuery.pre + jQuery.app + '/' + block_urn;
	
    /* Set default display type for block */
    if (!jQuery.BLOCK_REGISTER_DISPLAY[block_box_id]) {
        if (jQuery.BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME[block_name]) {
            jQuery.BLOCK_REGISTER_DISPLAY[block_box_id] = jQuery.BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME[block_name];
        } else {
            jQuery.BLOCK_REGISTER_DISPLAY[block_box_id] = "resource_list";
        }
    }

	$.ajax({
		type:'GET',
		url:url,
        dataType: 'application/xml',
        data : { display : jQuery.BLOCK_REGISTER_DISPLAY[block_box_id] },
		complete: function(r, s){
			
			if (s == "success") {
                
                // Invoke content rendering functions
                // * resource_list
                // * resource_list_with_details
                // * resource_list_as_icons
				var content = jQuery[jQuery.BLOCK_REGISTER_DISPLAY[block_box_id]]( block_box_id, r.responseText );

                // Push html content in page
				block_el.html( content );
                
                // Init dataTables
                // FIXME: currency ordering - must be shifted outside this generic function
                $('.dataTable').each(function() { $(this).dataTable({
                        'sPaginationType': 'full_numbers', 
                        "bServerSide": true,
                        "bStateSave": true,
                        "sAjaxSource": url + "edit_multiple",
                        "aoColumns": [
                            null,
                            null,
                            null,
                            { "sType": "currency" },
                            null
                        ]
                    }); 
                });
 
                // Set click handlers for actions
                block_el.find('.block_action').each(function () { 
                    $(this).click(function () { return jQuery.retrieve_form($(this))});
                });
                
				jQuery.post_load_handler(); // Update GUI event handlers
			}
			else {
				block_el.html( gettext("An error occurred while retrieving the data from server") );
			}
		}
	});	
}



//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.retrieve_form = function (action_el) {

    var action_name = action_el.html()
    var action_url = action_el.attr("href");
	
    var form_html = "";
    var form_script = "";

    var url = action_url;

    $.ajax({
        url : action_url, 
        success : function(d){

            //AAA TODO: do we need to decouple from admin?
            form_html = $(d).find('form');
            form_html.attr('action', action_url);
            form_html.find('.submit-row').each( function () { $(this).remove();});
            form_script = $(d).find('script');
        },
        async : false,
        dataType : "html"
    });

	//
	// Initialize dialog component
	//
	var options = { 
		success : function (responseText, statusText)  { 
            if (responseText.match('class="errorlist"')) {
                form_html = $(responseText).find('form');
                form_html.attr('action', action_url);
                form_html.find('.submit-row').each( function () { $(this).remove();});
                form_script = $(responseText).find('script');
                $(NEW_NOTE_DIALOG).html(form_html);
                eval(form_script);
            } 
            else {
                //
                // "hide"/close the dialog
                //
                $(NEW_NOTE_DIALOG).dialog('destroy');
                $(NEW_NOTE_DIALOG).dialog('close');

                window.location.reload();
				// response = jQuery.parseXml(responseText);
				// var resource_type = $(response).attr('resource_type');
				// var resource_id   = $(response).attr('resource_id');
				
                // var block_box_el = $(action_el).parentsUntil('li[block_name]');
                // if (block_box_el) {
                //     var block_name = block_box_el.attr('block_name');
                //     jQuery.GET_BLOCK_UPDATE_HANDLER(block_name)(block_box_id);
                // }
			}			
		}
	}		
	
	//
	// CREATE THE DIALOG
	//
    // Comment fero: use the same as global new_note form dialog
	$(NEW_NOTE_DIALOG).dialog('close');
	$(NEW_NOTE_DIALOG).dialog('destroy');
	
	$(NEW_NOTE_DIALOG).empty();
	$(NEW_NOTE_DIALOG).append(form_html);
    eval(form_script);
	
	var buttons = new Object();
	buttons[gettext('Confirm')] = function() {
		$(form_html).ajaxSubmit(options);
	};
	
//TODO fero gettext(action_name),
	$(NEW_NOTE_DIALOG).dialog({
		title: action_name,
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
};

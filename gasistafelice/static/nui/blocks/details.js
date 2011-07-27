
//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.open_new_note_form = function (note_action) {
	
	
	var form_html = NEW_NOTE_FORM_TEXT.replace("@@new_note_action@@", note_action);
	
	//
	// Initialize dialog component
	//
	var options = { 
		success     : function (responseText, statusText)  { 
			if (responseText.match('class="success"')) {
				response = jQuery.parseXml(responseText);
				var resource_type = $(response).attr('resource_type');
				var resource_id   = $(response).attr('resource_id');
				
				//jQuery.refreshBlock(resource_type, resource_id, 'details');
				
				var block_box_id = jQuery.BLOCK_BOX_ID(resource_type, resource_id,'details');
				
				jQuery.update_details_block(block_box_id);
			}			
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
	
};

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


//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

var SUSPEND_DIALOG = '#global_dialog_placeholder';

var SUSPEND_FORM   = '#suspend_form';
/*
 * 		<h3>" + gettext("Suspend resourse") + "</h3>\
		<br/>\
*/
var SUSPEND_FORM_TEXT= "\
		<div id='suspend_errors' style='color:red'></div> \
		\
		<form name='suspend_form' id='suspend_form' method='post' action='@@suspend_action@@'> \
			\
			<input type='radio' name='time_spec' value='forever' selected='selected'/> \
				" + gettext("Suspend forever") + " \
				<br/> \
			\
			<input type='radio' name='time_spec' value='seconds'/> \
				" + gettext("Suspend for") + "\
				<input name='seconds' type='text' value='3600'/> \
				" + gettext("seconds") + "\
				<br/> \
			\
			<input type='radio' name='time_spec' value='date'/> \
				" + gettext("Suspend until") + ": \
				<input style='width: 100px' id='resume_time' class='vDateField' type='text' name='resume_date' maxlength='10' value='@@date@@'/> \
				<input style='width: 100px' id='resume_hour' class='vTimeField' type='text' name='resume_hour' maxlength='8'  value='@@hour@@'/> \
				<br /> \
			\
			" + gettext("Reason") +":  <br /> \
			<textarea id='' name='reason'  cols='65' row='10' /> \
		</form>\
		";	
		
function format_date(d)
{
	return d.getDate() + "-" + d.getMonth() + "-" + d.getFullYear();
}

function format_time(d)
{
	var m = d.getMinutes();
	var s = d.getSeconds();
	if (m < 10)  m = '0'+m;
	if (s < 10)  s = '0'+s;
	return d.getHours() + ":" + m + ":" + s;
}
		
jQuery.suspend_resource = function (suspend_action) 
{
	
	ask_confirm(gettext("Are your sure you want to suspend this resource?"),
		function () {
			jQuery.show_suspend_form(suspend_action);
		}
		,
		function () { }
	);
};

jQuery.show_suspend_form = function(suspend_action) 
{
	var form_html = SUSPEND_FORM_TEXT;
	var errors  = '';
	
	var now = new Date();

	form_html = form_html.replace("@@suspend_action@@", suspend_action);
	form_html = form_html.replace("@@errors@@"        , errors);

	form_html = form_html.replace("@@date@@", format_date(now));
	form_html = form_html.replace("@@hour@@", format_time(now));
	
	//
	// Initialize dialog component
	//
	var options = { 
		success     : function (responseText, statusText)  { 
			if (responseText.match('class="success"')) {
				response = jQuery.parseXml(responseText);
				var resource_type = $(response).attr('resource_type');
				var resource_id   = $(response).attr('resource_id');

				$(SUSPEND_DIALOG).dialog('destroy');
				$(SUSPEND_DIALOG).dialog('close');

				//jQuery.refreshBlock(resource_type, resource_id, 'details');
				
				var block_box_id = jQuery.BLOCK_BOX_ID(resource_type, resource_id,'details');
				jQuery.update_details_block(block_box_id);
			}
			else {
				var response = $(jQuery.parseXml(responseText));
				var error_msgs = response.text();
				alert( error_msgs );
				
				$('#suspend_errors').empty();
				$('#suspend_errors').append(error_msgs + '<br/>');
			}	
		}
	}		
	
	//
	// CREATE THE DIALOG
	//
	$(SUSPEND_DIALOG).dialog('close');
	$(SUSPEND_DIALOG).dialog('destroy');
	
	$(SUSPEND_DIALOG).empty();
	$(SUSPEND_DIALOG).append(form_html);
	
	var buttons = new Object();
	buttons[gettext('Confirm')] = function() {
		//
		// "hide"/close the dialog
		//
		$(SUSPEND_FORM).ajaxSubmit(options);
	}	
	
	$(SUSPEND_DIALOG).dialog({
		title: gettext("Suspend parameters"),
		bgiframe: true,
		autoOpen: false,
		width: 600,
		height: "auto",
		modal: true,
		buttons: buttons,
		close: function() {
		}
	});
	
	$(SUSPEND_DIALOG).dialog('open');
	
	return false;
	
};

//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.resume_resource = function (sanet_urn) {


	ask_confirm(gettext("Are your sure you want to resume this resource?"),
		function () {

			var resume_url = jQuery.pre + "rest/" + sanet_urn + '/action/resume';	

			// Send the GET command and delete the row identified by "report_row_id"
			// if the GET is successful.
			jQuery.get(resume_url, function (responseText) {
				
				if (responseText.match('class="success"')) {
					response = jQuery.parseXml(responseText);
					var resource_type = $(response).attr('resource_type');
					var resource_id   = $(response).attr('resource_id');
					
					//jQuery.refreshBlock(resource_type, resource_id, 'details');
					
					var block_box_id = jQuery.BLOCK_BOX_ID(resource_type, resource_id, 'details');
					jQuery.update_details_block(block_box_id);
				}
			});
		}
		,
		function () {}
	);
	
	return false;

}

//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.create_details_block_content = function(data)
{


	function capitalize_str(s) {
		c = s.substring(0,1).toUpperCase();
		s = c + s.substring(1, s.length);
		return s;
	}
	
	var other_buttons = "\
	";


	var user_options_text = "\
		<div style='font-size: 0.8em;'>" + gettext("WARNING: some informations are omissed due to block's configuration") + ": <span style='color:red'>@@text@@ </span> </div> \
		";
		
			
	var suspend_button_template = "\
	<input type='button' onclick='jQuery.suspend_resource(\"@@suspend_action@@\")'  value='" + gettext('Suspend') + "' />\
	";

	var resume_button_template = "\
	<input type='button' onclick='jQuery.resume_resource(\"@@resource_urn@@\")'  value='" + gettext('Resume') + "' />\
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
								<span class='resource @@resource_type@@'>					\n\
									<a class='ctx_enabled' href='#rest/@@resource_type@@/@@resource_id@@/'>@@resource_descr@@</a> \n\
								</span>\n\
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
			<tr >\n\
				<td colspan='2'>\n\
					@@olap_part@@\n\
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
		<table border='0'> \n\
			<tr >\n\
				<td>\n\
					<input type='button' onclick='jQuery.open_new_note_form(\"@@new_note_action@@\")'  value='" + gettext("Add note")+ "' /> \n\
					@@other_buttons@@ \n\
				</td>\n\
			</tr>\n\
		</table>\n\
		\n\
		@@user_options@@\
		\
	</div>";
	
	
	olap_template = "\
		<table border='0'> \
			<tr >\
				<td>\
					<a href='@@olap_url@@'>Report Statistici</a>  \
				</td>\
			</tr>\
		</table>\
	";
	
	

	

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
				<a class='ctx_enabled resource @@resource_type@@ @@resource_status@@' \
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
		}
		if (val_type=='email') {
			val  = '<a href="mailto:' +val_obj.text() + '" > ' + val_obj.text() + '</a>';
		}
		else if (val_type == 'resourcelist') {
			
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
		else  if (val_type == 'node' || val_type == 'iface' || val_type == 'target' || val_type == 'measure') {
			val = '';
			var res = val_obj.find('resource');
			
			var rid    = res.attr('id');
			
			if (rid != "") {
				var rtype  = res.attr('type');
				var status = res.attr('status');
				var descr  = res.text();
				
				var urn   = rtype + "/" + rid;
				
				
				var e = resource_element;
				e = e.replace(/@@resource_type@@/g , rtype);
				e = e.replace(/@@resource_id@@/g   , rid);
				e = e.replace(/@@sanet_urn@@/g     , urn);
				e = e.replace('@@resource_descr@@' , descr);
				e = e.replace('@@resource_status@@', status);
				
				
				
				val += e;
			}
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
	
	// NOTES FORM
	new_note_action = jQuery.pre + "rest/" + sanet_urn + "/details/new_note";	
	details_template = details_template.replace('@@new_note_action@@', new_note_action);
	
	details_template = details_template.replace('@@notes_rows@@', notes_rows);
	
	//
	// OTHER BUTTONS
	//
	/*
	if (resource_type == 'measure' || resource_type == 'target' || resource_type == 'node') {
		other_buttons = other_buttons.replace(/@@resource_type@@/g, resource_type);
		other_buttons = other_buttons.replace(/@@resource_id@@/g  , resource_id);
		
		details_template = details_template.replace('@@other_buttons@@', other_buttons);
	}
	else {
		details_template = details_template.replace('@@other_buttons@@', '');
	}
	*/

	//
	// Calculate user actions
	//
	var other_buttons = [];
	
	var actions = jQel.find('content[type="user_actions"]');
	actions.find('action').each(function(){

		if ($(this).text() == 'suspend') {
			var action = jQuery.pre + "rest/" + sanet_urn + "/action/suspend";	
			var button = suspend_button_template;
			button = button.replace('@@suspend_action@@', action);	
			
			other_buttons.push(button);
		}
		if ($(this).text() == 'resume') {
			var button = resume_button_template;
			button = button.replace('@@resource_urn@@', sanet_urn);
			
			other_buttons.push(button );
		}
	})
	//
	//
	//
	details_template = details_template.replace('@@other_buttons@@', other_buttons.join(' ') );




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
	




	//
	// Olap integration
	//
	var url='';
	var olap_data = jQel.find('content[type="olap_data"]');
	olap_data.find('url').each(function(){ 
		url = $(this).text(); 
	});
	url = jQuery.trim(url);

	if (url != '')

		temp = olap_template.replace("@@olap_url@@", url);
	else
		temp = '';
	
	// Add element to the result
	details_template = details_template.replace('@@olap_part@@', temp );

	return details_template;
	

}







jQuery.update_details_block = function(block_box_id)
{
	var block_box_el = $('#' + block_box_id);
	var block_el  = block_box_el.children('.block_body');
	
	block_el.empty();
	
	var block_urn = block_box_el.attr('block_urn');
	
	var url = jQuery.pre + jQuery.app + '/' + block_urn;
	
	$.ajax({
		dataType:'plain/text',
		url:url,
		type:'GET',
		complete: function(r, s){
			
			
			
			if (s == "success") {
				var data = r.responseText;
				
				block_el.html( jQuery.create_details_block_content( data ) );
				
				jQuery.post_load_handler(); // Update GUI event handlers
			}
			else {
				block_el.html( gettext("An error occurred while retring the data from server") );
			}
		}
	});		
}

jQuery.REGISTER_BLOCK_UPDATE_HANDLER('details', jQuery.update_details_block);



jQuery.labsShowBlockConfigurationForm = function(form_data, block_urn) 
{
	return jQuery.xmppRender(form_data, "", block_urn, 1);
}

jQuery.labsShowBlockAddToUserPageForm = function(form_data, block_urn)
{
	return jQuery.xmppRender(form_data, "", block_urn, 0);
}


jQuery.xmppRender = function(form_data, form_additional_html_content, resource_block_id, config_only)
{
	var URL_CONFIG = jQuery.pre + "users/user/configblock/";
	var URL_ADD    = jQuery.pre + "users/userpage/0/add/";
	var URL_REMOVE = jQuery.pre + "users/userpage/0/remove/";
	
	
	var parts = resource_block_id.split('/');
	var resource_type = parts[0];
	var resource_id   = parts[1];
	var blockname     = parts[2];
	

	var e = $('#options_form');
	if (e != undefined) 
		e.empty();

	var jQel  = $(form_data);
	
	var title = jQel.find('xtitle').text();

	var form_container = $('<div id="opt_content_div"><form id="options_form">\n</form></div>');
	var form   = form_container.children('form');

	form.append(form_additional_html_content);
	form = form.append('<fieldset class="inner"></fieldset>').children();
	form = form.append('<table></table>').children();
	form = form.append('<tbody></tbody>').children();


	//
	// 
	//
	var tmp = jQel.find('field');
	if (tmp.length == 0){
		form.append("<tr><td>" + gettext("This block does not allow customization.") + "</td></tr>");
	}
	else{
		tmp.each(function(){
			var _ft   = $(this).attr('type');
			var _fl   = $(this).attr('label');
			var _fv   = $(this).attr('var');
			var _fval = $(this).children('value').text();
			

			var checked = '';
			if (_ft == 'checkbox')
				if (_fval == 'True')
					checked = 'checked="checked"';
			
			if(_ft != 'select')
				form.append("<tr><td><label>"+_fl+":</label></td><td><input type='"+_ft+"' name='"+_fv+"' value='"+_fval+"' " + checked + "/></td></tr>" );
			else
				form.append("<tr><td><label>"+_fl+":</label></td><td><select name='"+_fv+"'></select></td></tr>" );
		});
	}
    
	buttonlist_idx = {
		"Cancel": function(){
			form_container.dialog('close');
			form_container.empty();
		},
		"Ok":function(){
			var data = "";
			var dataitm = '<config>';
			
			$('#options_form').find('input').each( function(index, element){
				var type = $(element).attr('type');
				var name = $(element).attr('name');
				var val  = $(element).attr('value');
				//alert(name + " " + val);

				if (type == 'checkbox') {
					var checked  = $(element).attr('checked');
					if (checked == true)
						val = 'True';
					else
						val = 'False';
				}
					
				item = '<param name="' + name + '" value="' + val + '"/>';
				dataitm += item;
			});
			
			dataitm += "</config>";


			if (config_only == 0) {
				url = URL_ADD;
				//alert("ADDING");
			}
			else {
				url = URL_CONFIG;
				//alert("CONFIG");
			}

			$.post(url 
				,{
					 'resource_id'  : resource_id
					,'resource_type': resource_type
					,'blocktype'    : blockname
					,'data'         : dataitm
				}
				// success 
				, function (data, textStatus, XMLHttpRequest) {
					
					//
					// TODO: show errors in a better way
					//
					//alert(data);
					if (data.match('class="error"')) {
						//alert(data);
						return;
					}
					
					form_container.dialog('close');	
					form_container.empty();
				}				
			);

			
		}
	};

	if(location.hash.search('userpage')>0) {
		
		buttonlist_idx["Remove Block"] = function() {
			
			$.post( URL_REMOVE, {
				 'resource_id'  : resource_id
				,'resource_type': resource_type
				,'blocktype'    : blockname
			});
			
			form_container.dialog('close');
			
			alert(resource_block_id);
			
			//jQuery.removeBlock(resource_type, resource_id, blockname);
		}
	}

	//alert("showing config form -> " + resource_block_id);

	form_container.dialog({
		autoOpen: true,
		modal   : true,
		title   : title,
		width   : '450px',
		buttons : buttonlist_idx
	});
}


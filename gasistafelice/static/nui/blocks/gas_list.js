
jQuery.display_resource_list = function (element) {

	var res = "		\
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
	
	// nodes
	infos = jQel.find('content');
	
	if (infos.find('info').length > 0) {
	
		infos.find('info').each(function(){
			
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
//TODO fero: user actions
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
		res = gettext('There are no GAS related to this resource.');
	}

	return res;
}

jQuery.create_gas_list_block_content = function (element) {
	
    return jQuery.display_resource_list(element);
}

jQuery.REGISTER_BLOCK_UPDATE_HANDLER('gas_list', function(block_box_id) {});

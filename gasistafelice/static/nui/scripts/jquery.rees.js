
/* BLOCK_REGISTER_DISPLAY and BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME 
   are meant to store representation of blocks

   * BLOCK_REGISTER_DISPLAY is like block_box_id => display_type
   * BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME is like block_name => display_type 
     (block_name are keys registered in settings.RESOURCE_PAGE_BLOCKS)
     This acts as default display_type for block_box_id display type
*/

jQuery.BLOCK_REGISTER_DISPLAY = {}
jQuery.BLOCK_REGISTER_DISPLAY_DEFAULT_BY_NAME = {}

/* Display resource list */
/* This function is inspired by blocks specific code of SANET by Laboratori Guglielmo Marconi */
jQuery.resource_list = function (element) {

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
		res = gettext('There are no elements related to this resource.');
	}

	return res;
}

/* Display resource list with details */
jQuery.resource_list_with_details = function (element) {
    /* TODO */
}

/* Display resource list as icons */
jQuery.resource_list_as_icons = function (element) {
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
		complete: function(r, s){
			
			if (s == "success") {
                
				var content = jQuery[jQuery.BLOCK_REGISTER_DISPLAY[block_box_id]]( r.responseXML );
				block_el.html( content );
				jQuery.post_load_handler(); // Update GUI event handlers
			}
			else {
				block_el.html( gettext("An error occurred while retrieving the data from server") );
			}
		}
	});	}


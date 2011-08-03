
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

/* jQuery.BLOCKS are used to store Block instances.
   They will be retrieved by the update procedure
 */

jQuery.BLOCKS = {};

/*******************************
 * User Interface Block class
 *******************************/

jQuery.UIBlock = Class.extend({

    init: function(block_name) {
        this.block_name = block_name;
        this.active_view = "view";

        //HACK to be compatible with SANET block management
        //TODO: blocks handler calls as pure objects
        //(i.e. check block registered in jQuery.BLOCKS and call update_handler)
        jQuery.REGISTER_BLOCK_UPDATE_HANDLER(block_name, function (block_box_id) {
            var block_instance = jQuery.BLOCKS[block_name];
            return block_instance.update_handler(block_box_id);
        });

    },

    set_parsed_data: function(data) {
        var jQel = jQuery(jQuery.parseXml(data));
        if (jQel.children('error').length > 0)
            return jQel.text()
        this.parsed_data = jQel;
    },

    update_handler: function(block_box_id) {

        this.block_box_id = block_box_id;

        var block_box_el = $('#' + block_box_id);
        this.block_el = block_box_el.children('.block_body');
        this.block_el.empty();
        
        var block_urn = block_box_el.attr('block_urn');
        this.url = jQuery.pre + jQuery.app + '/' + block_urn;

        var block_obj = this;
        
        $.ajax({
            type:'GET',
            url: block_obj.url,
            dataType: 'application/xml',
            data : { render_as : block_obj.rendering },
            complete: function(r, s){
                
                if (s == "success") {
                    
                    block_obj.update_content(r.responseText);
                    block_obj.post_load_handler(); // Update GUI event handlers
                }
                else {
                    block_obj.block_el.html( gettext("An error occurred while retrieving the data from server") );
                }
            }
        });	
    },  

    update_content: function(data) {

        var errors = this.set_parsed_data(data);

        if (errors) {
            this.block_el.html(content);
            return;
        }

        //Render block content
        var content = this.render_actions(data);
        content += this.render_content(data);

        // Push HTML content in page
        // After this moment is possible to update event handlers
        this.block_el.html(content);

        // Set click handlers for actions
        var block_obj = this;
        this.block_el.find('.block_action').each(function () { 
            $(this).click(function () { return block_obj.action_handler($(this))});
        });
    },

    post_load_handler : function() {
        jQuery.post_load_handler();
    },

    action_handler : function(action_el) {

        this.active_view = action_el.attr('name');
        if (action_el.attr('popup_form') == "1") {
            return jQuery.retrieve_form(action_el);
        }
        this.update_handler(this.block_box_id);
        return false;
    },

    render_actions : function(data) {

        var res = "<div class='list_actions'>@@list_actions@@</div>";
        
        var jQel = this.parsed_data;
        
        // Resource ID
        var resource_type =  jQel.attr('resource_type');
        var resource_id   =  jQel.attr('resource_id');
        
        //Render block actions
        var contents = jQel.find('content[type="user_actions"]');
        var action_template = "<a href=\"#\" url=\"@@action_url@@\" class=\"block_action\" name=\"@@action_name@@\" popup_form=\"@@popup_form@@\">@@action_verbose_name@@</a>";
        var actions = '';

        if (contents.find('action').length > 0) {
        
            contents.find('action').each(function(){
                var action = action_template.replace(/@@action_name@@/g, $(this).attr("name"));
                action = action.replace(/@@action_verbose_name@@/g, $(this).attr("verbose_name"));
                action = action.replace(/@@action_url@@/g, $(this).attr("url"));
                action = action.replace(/@@popup_form@@/g, $(this).attr("popup_form"));
                actions += action;
            });
        }

        res = res.replace('@@list_actions@@', actions);
        return res;
    
    },
    
    render_content : function(data) {
        //TODO fero: To be filled with ... details block?!?
    }

});


/***************************
 * Block with list class
 **************************/

jQuery.UIBlockWithList = jQuery.UIBlock.extend({

    init: function(block_name, default_rendering) {

        if (!default_rendering)
            default_rendering = "list";

        this.default_rendering = default_rendering;
        this.rendering = default_rendering;
        this._super(block_name);
    },

    update_content: function(data) {
        this._super(data);
        
    },

    post_load_handler: function() {
        this["rendering_"+this.rendering+"_post_load_handler"]();
        this._super();
    },

    rendering_list_post_load_handler: function () {},
    rendering_icons_post_load_handler: function () {},
    rendering_table_post_load_handler: function () {},

    render_content: function(data) {
        return this["render_content_as_"+this.rendering](data);
    },

    render_content_as_table: function(data) {
        // Render block content as table

        var jQel = this.parsed_data;

        // Resource ID... we could need them later... TODO fero TOCHECK
        var resource_type =  jQel.attr('resource_type');
        var resource_id   =  jQel.attr('resource_id');
        
        // Find table and render
        var html_table = jQel.find('content[type="table"]').html();

        //Prepare form
        var res = html_table;

        if (this.active_view == "edit_multiple") {
            var action_url = this.url + this.active_view;
            res = "<form id=\"" + this.block_box_id + "-form\" method=\"POST\" action=\""+action_url+"\">";
            res += "<input type=\"submit\" name=\"" + gettext('Submit') + "\" />";
            res += html_table;
            res += "</form>";
        }

        return res;
        
    },

    render_content_as_icons: function(data) {

    },

});


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





/* Retrieve and update blocks that include resource list */
jQuery.resource_list_block_update = function(block_box_id) {

}


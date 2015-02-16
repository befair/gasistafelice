
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

jQuery.render_bool = function (val) {
    var rv;
    if (val.trim().toLowerCase() == "false") {
        rv = '<img alt="False" src="/media/img/admin/icon-no.gif">';
    } else if (val.trim().toLowerCase() == "true") {
        rv = '<img alt="True" src="/media/img/admin/icon-yes.gif">';
    } else {
        alert("Variable of boolean type has nor true or false value");
    }
    return rv;
}

/* Resource management facitilies */
jQuery.Resource = Class.extend({

    init : function(urn, name, more_details) {
        this.urn = urn;
        this.type = urn.split('/')[0];
        this.id = urn.split('/')[1];
        this.url = "#rest/"+urn;
        this.absolute_url = jQuery.pre + "rest/"+urn;
        this.name = name;
        this.more_details = more_details || false;
    },

    render : function() {
        if (this.name == undefined) {
            alert(gettext('Please provide a name for this resource before rendering it'));
        }
        var res = "";

        //AAAAA FIXME TODO: ancora non è implementata la pagina della risorsa categoria
        //TOGLIERE L'IF QUANDO SARà IMPLEMENTATA
        if ((this.type == 'productcategory')|| (this.type == 'delivery')|| (this.type == 'withdrawal')) { 
            res = this.name;
        } else {
            res = "<a class='ctx_enabled resource inline @@resource_type@@' sanet_urn='@@urn@@' href='@@url@@'> @@name@@</a>@@more_details@@";
            res = res.replace(/@@resource_type@@/g, this.type);
            res = res.replace(/@@name@@/g, this.name);
            res = res.replace(/@@urn@@/g,  this.urn);
            res = res.replace(/@@url@@/g, this.url);
            if (this.more_details) {
                res = res.replace(/@@more_details@@/g, '<p>' + this.more_details + '</p>');
            } else {
                res = res.replace(/@@more_details@@/g, '');
            }
        }
        return res;
    },

});
    
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
        this.default_view = this.active_view;
        this.extra_queryString = '';

        //HACK to be compatible with SANET block management
        //TODO: blocks handler calls as pure objects
        //(i.e. check block registered in jQuery.BLOCKS and call update_handler)
        jQuery.REGISTER_BLOCK_UPDATE_HANDLER(block_name, function (block_box_id) {
            var block_instance = jQuery.BLOCKS[block_name];
            return block_instance.update_handler(block_box_id);
        });

    },

    get_control_panel: function() {
        
        var block_el = $('#' + this.block_box_id);
        var block_urn = block_el.attr('block_urn');
        this.url = jQuery.pre + jQuery.app + '/' + block_urn;
        
        var block_obj = this;

        $.ajax({
            type:'GET',
            url: block_obj.url + 'options',
            dataType: 'xml',
            async: false,
            complete: function(r, s){
                
                if (s == "success") {
                    
                    var jQel = jQuery(jQuery.parseXml(r.responseText));
                    if (jQel.children('error').length > 0)
                        return jQel.text()


                    if (jQel.find('field').length) {
                        var form_container = $('<div class="opt_content_div"><form id="'+ block_obj.block_name + '-options_form">\n</form></div>');
                        var form   = form_container.children('form');

                        form = form.append('<fieldset class="inner"></fieldset>').children();
                        form = form.append('<table></table>').children();
                        form = form.append('<tbody></tbody>').children();

                        jQel.find('field').each( function () {
                            var _ft   = $(this).attr('type');
                            var _fv   = $(this).attr('var');
                            var _fval = $(this).children('value').text();
                            var _fl   = $(this).attr('label');
                            var urn   = $(this).attr('urn');
                            if (urn != undefined) {
                                //Display field label as usual
                                _fl = new jQuery.Resource(urn, _fl).render();
                            }
                            
                            var checked = '';
                            if ((_ft == 'checkbox')||(_ft == 'radio')) {
                                var _fchk = $(this).children('value').attr('xselected');
                                if (_fchk == 'True')
                                    checked = 'checked="checked"';
                            }
                            
                            if(_ft != 'select')
                                form.append("<tr><td><input type='"+_ft+"' name='gfCP_"+_fv+"' value='"+_fval+"' " + checked + "/></td><td><label>"+_fl+"</label></td></tr>" );
                            else
                                form.append("<tr><td><label>"+_fl+":</label></td><td><select name='gfCP_"+_fv+"'></select></td></tr>" );
                        });

                        //KO: block_el.prev('.block_control_panel').html(form_container);
                        //    because block is not in page yet!
                        block_el.find('.block_control_panel').first().html(form_container);

                        block_el.parent().find('.opt_content_div input').each( function () {
                            $(this).change(function (e) {
                                block_obj.extra_queryString = $('#'+ block_obj.block_name + '-options_form').serialize();
                                block_obj.update_handler(block_obj.block_box_id);
                            })
                            block_obj.extra_queryString = $('#'+ block_obj.block_name + '-options_form').serialize();
                        });

                      }
                }
                else {
                    block_el.html( gettext("An error occurred while retrieving the data from server (" + s +")") );
                }
            }
        });	
    },

    get_data_source : function() {
        var more = '';
        if (this.extra_queryString) {
            more = '&' + this.extra_queryString;
        }
        return this.url + this.active_view + '?render_as=' + this.rendering + more;
    },
    set_parsed_data: function(data) {
        var jQel = jQuery(jQuery.parseXml(data));
        if (jQel.children('error').length > 0)
            return jQel.text()
        this.parsed_data = jQel;

        //TODO: to be renamed as "urn"
        var urn = jQel.attr('sanet_urn');
        if (urn == undefined) {
            var urn = jQel.attr('resource_type') + "/" + jQel.attr('resource_id');
        }
        
        this.resource = new jQuery.Resource(urn);
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
            dataType: 'xml',
            data : { render_as : block_obj.rendering },
            complete: function(r, s){
                
                if (s == "success") {
                    
                    block_obj.update_content(r.responseText);
                    block_obj.post_load_handler(); // Update GUI event handlers
                }
                else {
                    block_obj.block_el.html( gettext("An error occurred while retrieving the data from server (" + s +")") );
                }
            }
        });	
    },  

    update_content: function(data) {

        var errors = this.set_parsed_data(data);

        if (errors) {
            alert('qui abbiamo un bug');
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

        var method = action_el.attr('method');

        if (method && 
            method.toUpperCase() == "OPENURL"
        )
            window.open(action_el.attr('url'), "_blank");
            //this break execution...
            
        //-- else...

        /* TODO: action attribute "on_complete" can assume values
        /* reload_page, switch_view, reload_block, 
        if action_el.attr('on_complete')
        */
        var name = action_el.attr('name');

        if (action_el.attr('popup_form') == "1") {
            return jQuery.retrieve_form(action_el);

        } else if ((name == "edit_multiple")||(name=="view")) {
            if (this.active_view != name) {
                this.active_view = name;
                this.update_handler(this.block_box_id);
                //Reload dataTable
                /*var dt_holder = this.block_el.find('.dataTable')
                this.dataTable = dt_holder.dataTable({
                    "sAjaxSource" : this.url + this.active_view + "?render_as=table",
                    "bDestroy": true,
                });*/
                //this.dataTable.fnClearTable( 0 );
                //this.dataTable.fnDraw();
            }

        } else {

            if (method.toLowerCase() == "get")
                method = "get";
            else
                method = "post";

            var accept = true;
            var confirm_text = action_el.attr('confirm_text');
            if (confirm_text) {
                accept = confirm(confirm_text);
            }

            if (accept) {
                //TODO: Notify user success/failure
                $[method](action_el.attr("url"));
                this.update_handler(this.block_box_id);
            }
        }

        return false;
    },

    render_actions : function(data) {

        var res = "<div class='list_actions'>@@list_actions@@</div>";
        
        var jQel = this.parsed_data;
        
        //Render block actions
        var contents = jQel.find('content[type="user_actions"]');
        var action_template = "<input type='button' href=\"#\" url=\"@@action_url@@\" class=\"block_action\" name=\"@@action_name@@\" popup_form=\"@@popup_form@@\" value=\"@@action_verbose_name@@\" method=\"@@action_method@@\" confirm_text=\"@@confirm_text@@\" />";
        var actions = '';

        if (contents.find('action').length > 0) {
        
            contents.find('action').each(function(){
                var action = action_template.replace(/@@action_name@@/g, $(this).attr("name"));
                action = action.replace(/@@action_verbose_name@@/g, $(this).attr("verbose_name"));
                action = action.replace(/@@action_url@@/g, $(this).attr("url"));
                action = action.replace(/@@popup_form@@/g, $(this).attr("popup_form"));
                action = action.replace(/@@action_method@@/g, $(this).attr("method"));
                action = action.replace(/@@confirm_text@@/g, $(this).attr("confirm_text"));
                actions += action;
            });
        }

        res = res.replace('@@list_actions@@', actions);
        return res;
    
    },
    
    render_content : function(data) {
        // to be defined in subclasses (see: blocks/details.js
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
        this.submit_name = gettext('Submit');
        this._super(block_name);
    },

    update_content: function(data) {
        this._super(data);
        
    },

    post_load_handler: function() {
        this["rendering_"+this.rendering+"_post_load_handler"]();
        this._super();
    },

    form_success_process_json : function(form_el, data) {
            //JSON data answered by server side code. The dict holds errors.
            //If no errors found: reset active_view and reload.
            //If errors found: write down errors in form

            if (!data['error_msg'].length) {
                //No errors found
                this.active_view = this.default_view;
                this.update_handler(this.block_box_id);

            } else {
                var error_list_html = '<ul class="errorlist">';
                var stop_it = false;
                for (var i=0; i<data['error_msg'].length; i++) {
                    var error_d = data['error_msg'][i];
                    if (!jQuery.isEmptyObject(error_d)) {
                        var n = i+1;
                        var error_html = '<li>Riga ' + n + ' - ';
                        for (var item in error_d) {
                            if (item != "__all__") {
                                error_html += item + " " + error_d[item];
                            } else {
                                error_html += error_d[item];
                                stop_it = true;
                            }
                        }
                        error_list_html += error_html + "</li>";
                        if (stop_it)
                            break
                    }
                }
                error_list_html += "</ul>";
                form_el.prepend(error_list_html);
            }

            //TODO: #user_notifications should be filled with appropriate message

    },

    form_beforeSubmit : function (form_el, formData, jqForm, options) { 

            form_el.find('.errorlist').remove();

            //set formset management fields:
            //https://docs.djangoproject.com/en/dev/topics/forms/formsets/#understanding-the-managementform
    },

    rendering_list_post_load_handler: function () {},
    rendering_icons_post_load_handler: function () {},
    rendering_table_post_load_handler: function () {

        var block_instance = this;
        if (this.active_view == "edit_multiple") {
            var form_id = this.block_box_id + "-form";
            $('#' + form_id).submit( function() {

                var form_el = $(this);
                var options = {
                    dataType:  'json',
                    beforeSubmit: function (formData, jqForm, options) {
                        block_instance.form_beforeSubmit(form_el, formData, jqForm, options);
                    },
                    success : function(data) {
                        return block_instance.form_success_process_json(form_el, data);
                    }
                }

                $(this).ajaxSubmit(options);

                return false;

//                //FIXME: this serialize MUST be applied to form widgets of all table nodes:
//                //get them with oTable.fnGetNodes() 
//                var sData = $(this).serialize();
//                alert( "The following data would have been submitted to the server: \n\n"+sData );
                
            });
        }
    },

    render_content: function(data) {
        return this["render_content_as_"+this.rendering](data);
    },

    render_content_as_table: function(data) {
        // Render block content as table

        var jQel = this.parsed_data;

        // Find table and render
        var html_table = jQel.find('content[type="table"]').html();

        //Prepare form
        var res = html_table;

        if (this.active_view == "edit_multiple") {
            var action_url = this.url + this.active_view;
            var form_id = this.block_box_id + "-form";
            res = "<form id=\"" + form_id +"\" method=\"POST\" action=\""+action_url+"\">";
            res += "<input type=\"submit\" name=\"submit\" value=\"" + this.submit_name + "\" />";
            res += html_table;
            res += "<input type=\"submit\" name=\"submit\" value=\"" + this.submit_name + "\" />";
            res += "<input type=\"hidden\" name=\"form-TOTAL_FORMS\" value=\"2\" id=\"" + form_id + "-TOTAL_FORMS\" />";
            res += "<input type=\"hidden\" name=\"form-INITIAL_FORMS\" value=\"0\" id=\"" + form_id + "-INITIAL_FORMS\" />";
            res += "<input type=\"hidden\" name=\"form-MAX_NUM_FORMS\" id=\"" + form_id + "-MAX_NUM_FORMS\" />";
            res += "</form>";
        }

        return res;
        
    },

    render_content_as_icons: function(data) {

    },

    render_content_as_list: function(data) {
        // Display resource list

        /* This method is inspired by blocks specific code of SANET by Laboratori Guglielmo Marconi */

        var res = "		\
        <table> 		\
            @@inforow@@	\
        </table> 		\
        ";
        
        var inforow = " \
            <tr id='@@row_id@@' > 			\
                <td width='100%'>   			\
                    <span class='resource row' >@@resource@@</span> \
                </td>		     			\
                <td>		     			\
                @@actions@@ \
                </td>		     			\
            </tr>	 			\
            @@inforow@@ \
        ";

        var jQel = this.parsed_data;
        
        if (jQel.children('error').length > 0)
            return jQel.text()
        if (jQel.children('sysmsg').length > 0) 
            return jQel.text()
            
        
        // Resource ID
        var resource_type =  jQel.attr('resource_type');
        var resource_id   =  jQel.attr('resource_id');
        
        // Resources
        var contents = jQel.find('content[type="list"]');
        
        if (contents.find('info').length > 0) {
        
            contents.find('info').each(function(){
                
                var name = $(this).attr('name');
                var urn = $(this).attr('sanet_urn');
                var more_details = $(this).attr('more_details');
                var row_id = resource_type + '_row_' + urn.split('/').join('_');

                var a = inforow
                a = a.replace(/@@row_id@@/g, row_id);
                
                a = a.replace(/@@resource@@/g, new jQuery.Resource(urn, name, more_details).render());

                var actions = '<ul style="display:table">';
                //WAS LF: this is just a link, not an action
                //var action_template = "<a href=\"#\" url=\"@@action_url@@\" class=\"block_action\" name=\"@@action_name@@\" popup_form=\"@@popup_form@@\" title=\"@@action_title@@\">@@action_html@@</a>";
                var action_template = "<li style=\"display:table-cell;\"><a href=\"@@action_url@@\" name=\"@@action_name@@\" in_popup=\"@@in_popup@@\" title=\"@@action_title@@\">@@action_div@@</a></li>";
                var action_div = "<div class=\"row_action\" style=\"background-image: url('@@background_url@@');\"> </div>";

                $(this).find('info_action').each(function() {

                    var action = action_template.replace(/@@action_name@@/g, $(this).attr("name"));
                    action = action.replace(/@@action_title@@/g, $(this).attr("title"));
                    action = action.replace(/@@action_url@@/g, $(this).attr("url"));
                    action = action.replace(/@@in_popup@@/g, $(this).attr("in_popup")||0);
                    var this_action_div = action_div.replace(/@@background_url@@/g, $(this).attr("background_url"));
                    action = action.replace(/@@action_div@@/g, this_action_div);
                    actions += action;
                });
                actions += "</ul>"

                a = a.replace(/@@actions@@/g, actions);		

                res = res.replace('@@inforow@@', a);
            });
            
            res = res.replace('@@inforow@@', '');	
        }
        else {
            res = res.replace('@@inforow@@', gettext('There are no elements related to this resource.'));
        }

        return res;
    },
});




//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.retrieve_form = function (action_el) {

    var action_name = action_el.val();
    var action_url = action_el.attr("url");
	
    var url = action_url;

    var res = $.ajax({
        url : action_url, 
        async : false,
        dataType : "xml" //xml needed to evaluate script by hand later
    });

    var d = $(res.responseText);
    var jqMessagelist = d.find('.messagelist');
    var jqForm = d.find('form');
    jqForm.attr('action', action_url);
    jqForm.find('.submit-row').each( function () { $(this).remove();});
    var form_script = d.find('script');

	//
	// Initialize dialog component
	//
	var options = { 
		success : function (responseText, statusText)  { 
            if (responseText.match('class="errorlist"')) {
                jqMessagelist = $(responseText).find('.messagelist');
                jqForm = $(responseText).find('form');
                jqForm.attr('action', action_url);
                jqForm.find('.submit-row').each( function () { $(this).remove();});
                form_script = $(responseText).find('script');
                $(NEW_NOTE_DIALOG).html(jqForm);
                //-- LF: it should be needed only if there are <script> tags outside <form>
                //eval(form_script);
            } 
            else {
                //
                // "hide"/close the dialog
                //
                $(NEW_NOTE_DIALOG).dialog('destroy');
                $(NEW_NOTE_DIALOG).dialog('close');
                update_page();
                //
                //
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
	$(NEW_NOTE_DIALOG).append(jqMessagelist);
	$(NEW_NOTE_DIALOG).append(jqForm);
    //-- LF: it should be needed only if there are <script> tags outside <form>
    //eval(form_script);
	
	var buttons = new Object();
	buttons[gettext('Confirm')] = function() {
		$(jqForm).ajaxSubmit(options);
	};
	
	$(NEW_NOTE_DIALOG).dialog({
		title: gettext(action_name),
		bgiframe: true,
		autoOpen: false,
		width: 600,
		height: "auto",
		modal: true,
		buttons: buttons,
		close: function() { }
	});
	
	$(NEW_NOTE_DIALOG).dialog('open');
    $(window).trigger('init-autocomplete');
	return false;
};





/* Retrieve and update blocks that include resource list */
jQuery.resource_list_block_update = function(block_box_id) {
    alert("vecchia gestione blocco "+block_box_id); 
}

//------------------------------------------------------------------------------//
//                          Utils functions for some blocks                     //
//------------------------------------------------------------------------------//

function fncOrder(x, _step, _min, _price, _blk){
  try {
    var el = null;
    _step > 0 ? (el = x.prev('input')) : (el = x.next('input'));
    var qta = parseFloat(el.val().replace(',','.')); 
    var prev_row_total = parseFloat(qta*_price);
    var new_qta = 0
    if (_step > 0)
        qta == 0 ? (new_qta = _min) : (new_qta = qta + _step);
    else
        qta <= _min ? (new_qta = 0) : (new_qta = qta + _step);
    el.val(SetFloat(new_qta))
    var next_td = x.parent('td').next(); 
    var row_total = new_qta * _price;
    next_td.html('€ ' + SetFloat(row_total));
    var total = parseFloat($(_blk).html().substr(2).replace(',','.')) + row_total - prev_row_total;
    $(_blk).html('€ ' + SetFloat(total));
    }
  catch(e){//alert(e.message);
    }
  return false;
};
function SetFloat(_qta){
    //return String(' ' + GetRoundedFloat(_qta)).replace('.',',') Ko DECIMAL_SEPARATOR = ',' in clean_data()
    return GetRoundedFloat(_qta);
}
function GetRoundedFloat(v) {
    if (v == 0) { return 0; }
    if (v.toString().indexOf('.') == -1) { return v; }
    return ((v.toFixed) ? v.toFixed(2) : (Math.round(v * 100) / 100));
}
function checkall(chk){
$(chk).parents('table:eq(0)').find(':checkbox').attr('checked', chk.checked);
}

//---------------------------------------------
// Clock
//---------------------------------------------
jQuery.Clock = Class.extend({

    init : function (jQel, interval) {

        this.jQel = jQel;
        this.interval = interval;
        if (this.interval == undefined)
            this.interval = 1;
        
        this.is_set = false;
        
    },

    set_start : function(now) {
        //Takes in input a string like 
        //mar 01 nov 2011 18:49:44 
        //which is split into prefix + hh:mm:ss

        this.start = now;
        rnow = now.trim().split(' ').reverse().join(' ');
        i = rnow.indexOf(':')
        this.hh = parseInt(rnow.slice(0, i));
        rnow = rnow.slice(i+1);
        i = rnow.indexOf(':')
        this.mm = parseInt(rnow.slice(0, i));
        rnow = rnow.slice(i+1);
        this.ss = parseInt(rnow.slice(0, i));
        i = rnow.indexOf(' ')
        this.prefix = rnow.slice(i+1).trim().split(' ').reverse().join(' ');
        this.is_set = true;
        
    },

    update : function() {
        if (this.is_set == true) {
            this.ss = this.ss + this.interval;
            var ss_mod  = this.ss%60;
            this.mm = this.mm + (this.ss-ss_mod)/60;
            var mm_mod  = this.mm%60;
            this.hh = this.hh + (this.mm-mm_mod)/60;
            if (this.hh == 24) {
                //Do not change day now
                this.hh = 0;
            }
            this.mm = mm_mod;
            this.ss = ss_mod;

            var s = this.prefix+' ';
            if (this.hh<10) s += '0';
            s += this.hh + ':';
            if (this.mm<10) s += '0';
            s += this.mm + ':';
            if (this.ss<10) s += '0';
            s += this.ss;
            
            this.jQel.html(s);
        }
    }
});
        

var FADE_LEVEL = 0.60;
var FADE_TIME_MS = 1500;

jQuery.app_stop_loading = function(el) {
    if (el === undefined) {
        el = $('#loading-container');
    }
    el.hide();
};
jQuery.app_stop_loading_action = function(el) {
    //jQuery.labsglobals.action_is_loading = false;
    jQuery.app_stop_loading(el);
};

jQuery.app_is_loading = function (el) {
    if (el === undefined) {
        el = $('#loading-container');
    }
    var h = $(window).height();
    var w = $(window).width();
    el.css('top', -100 + parseInt($(window).scrollTop(), 10));
    el.css('left', -100 + parseInt($(window).scrollLeft(),10));
    var lh = $('#loading-msg').css('height');
    var lw = $('#loading-msg').css('width');
    $('#loading-msg').css('top', parseInt(h,10)/2-parseInt(lh,10)/2);
    $('#loading-msg').css('left', parseInt(w,10)/2-parseInt(lw,10)/2);
    el.show();
    $('#loading-msg').fadeTo(FADE_TIME_MS, FADE_LEVEL, jQuery.toggleFade);
};


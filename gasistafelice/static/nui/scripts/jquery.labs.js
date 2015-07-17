//==============================================================================
// Django's i18n function wrapper.
//==============================================================================

$._ = function(msgid) {
	x = gettext(msgid);
	//alert(msgid + '->' + x);
	return x;
}

$._ = function(msgid) {
	x = gettext(msgid);
	//alert(msgid + '->' + x);
	return x;
}

//==============================================================================
// JSON shortcut
//==============================================================================

$.JSON = JSON;


//==============================================================================
// Dynamic Block handling
//==============================================================================

// Hashtable of loaded javascript files indexed by 'src'.
// If a 'src' is present, the javascript file is already loaded.
jQuery.loadedBlockSrcLoaded  = new Array();

// Hashtable of blocks' update handler
jQuery.loadedBlockUpdate     = new Array();     // List of update

// List of blocks waiting for the related javascript file
jQuery.pendingBlocks         = new Array();


jQuery.BLOCK_BOX_ID = function( resource_type, resource_id, block_name )
{
	return 'block_' + jQuery.app + '_'+ resource_type +'_'+ resource_id +'_'+ block_name + '_box';
}

jQuery.REGISTER_BLOCK_UPDATE_HANDLER = function(block_name, update_handler)
{
	var id = block_name + '_block_update';
	jQuery.loadedBlockUpdate[id] = update_handler;
}

jQuery.GET_BLOCK_UPDATE_HANDLER = function(block_name)
{
	var handler_name = block_name + "_block_update";
	return jQuery.loadedBlockUpdate[handler_name];
}

jQuery.set_block_script_loaded = function(block_name)
{
	var src_path  = "/static/nui/blocks/"+block_name+".js";
	jQuery.loadedBlockSrcLoaded.push( src_path );
}

jQuery.is_block_script_loaded = function(block_name)
{
	var src_path  = "/static/nui/blocks/"+block_name+".js";
	return ($.inArray(src_path, jQuery.loadedBlockSrcLoaded) > -1);
}


jQuery.load_block_script = function (block_name, on_load_callback )
{
	if (jQuery.is_block_script_loaded(block_name)) {
		on_load_callback(block_name);
		return
	}

	var src_path  = "/static/nui/blocks/"+block_name+".js";

	// Force the current page to download the javascript file
	var head = $('HEAD')[0];

	var script = document.createElement("script");
	script.type = "text/javascript";
	script.src  = src_path;

	script.onload             = function(){
		/* FIREFOX, CHROME */
		jQuery.set_block_script_loaded( block_name );
 		on_load_callback(block_name);
	}

	script.onreadystatechange = function () {
		/* IE 8 */
		//alert("onreadystatechange " + this.readyState);
      		if (this.readyState == 'loaded') {
			jQuery.set_block_script_loaded( block_name );
			on_load_callback(block_name);
      		}
   	}

	head.appendChild(script);
}

jQuery.add_pending_block=function( script_src, block_id )
{
	jQuery.pendingBlocks.push( { script_src: script_src, block_id : block_id } );
}

jQuery.showBlock = function(block_box_id, force_update)
{
	var block_name = $('#'+block_box_id).attr('block_name');

	var is_loaded = jQuery.is_block_script_loaded(block_name);

	if (is_loaded == false) {

		var src_path  = "/static/nui/blocks/"+block_name+".js";

		// Remember informations about the unrendered block
		jQuery.add_pending_block(src_path, block_box_id);

		// Dinamicaly download the javascript and remember to
		// render the pending blocks when download is completed.
		var onload_completed = function(){

			//var loaded_src_path = this.attributes['src'].value;
			// We are sure the script is loaded
			jQuery.set_block_script_loaded( block_name );

			// Launch script for every pending block which requires
			// the same script.
			for (var i=0; i < jQuery.pendingBlocks.length; i++) {
				if(jQuery.pendingBlocks[i].script_src == src_path) {
					jQuery.updateBlockContent(jQuery.pendingBlocks[i].block_id, true); // force update
				}
			}
		}

		// Force the current page to download the javascript file
		var head = $('HEAD')[0];

		var script = document.createElement("script");
		script.type = "text/javascript";
		script.src  = src_path;
		script.onload = onload_completed;
		script.onload = function () {
      			/*if (this.readyState == 'complete') */
      				onload_completed();
   		}

		head.appendChild(script);
	}
	else {
		jQuery.updateBlockContent(block_box_id, force_update);
	}
}

jQuery.updateBlockContent = function(block_box_id, force_update)
{
	var block_name = $('#' + block_box_id).attr('block_name');

	var start_handler = jQuery.GET_BLOCK_UPDATE_HANDLER(block_name);

	if ( start_handler ) {

		start_handler(block_box_id, force_update);

		// Perform global event bindings
		jQuery.post_load_handler();
	}
	else {
		alert('No update handler defined for "'+ block_name+'"');
	}
}


jQuery.removeBlock = function(rtype, rid, tname)
{
        var resource_path = "rest/"+rtype+"/"+rid+"/"+tname+"/";
        var node_selector = '.block[sanet_url='+resource_path+']';

        $(node_selector).remove();
};

function get_block_parameter(block_id, name)      { return $('#'+block_id).attr(name); }
function set_block_parameter(block_id, name, val) { $('#'+block_id).attr(name, val);   }


//==============================================================================
// SANET COOKIES
//==============================================================================

var SANET_COOKIE_EXPIRATION_TIME = new Date(2038, 1, 1);

function save_block_attribute(block_name, attribute_name, value)
{
	var cookie_name = block_name + "_" + attribute_name;

	$.cookie(cookie_name, value, { path: '/', expires: SANET_COOKIE_EXPIRATION_TIME } );
}

function get_block_attribute(block_name, attribute_name)
{
	var cookie_name = block_name + "_" + attribute_name;

	return $.cookie(cookie_name);
}

//==============================================================================
// TIMERS FUNCTIONS
//==============================================================================


function add_new_timer(timers, callback_function, interval)
{
	var ONE_SECOND = 1000;

	var timer_id = setInterval( callback_function, interval * ONE_SECOND);

	// Add new timer
	timers.push( timer_id );
}

function clear_all_timers(timers)
{
	// Unset timers
	while (timers.length > 0) {
		timer_id = timers.shift();
		clearInterval( timer_id );
	}
}

function start_generic_update_timer(timers, url, timeout, node_css_selector, pre_update_handler, post_update_handler)
{
	pre_update_handler  = pre_update_handler ==null ? function(){} : pre_update_handler;
	post_update_handler = post_update_handler==null ? function(){} : post_update_handler;

	var update_code = function() {

		pre_update_handler();
		$.ajax({
			type:'GET',
			//url:jQuery.pre + resource,
			url: url,
			dataType:'text',
			complete:function(r,s){
				if (s == 'success') {
					var t = r.responseText;
					$(node_css_selector).html(t);
					post_update_handler();
				}
				else {
					$(node_css_selector).html("ERROR on GET " + url);
				}
			}
		});
	}

	// Update the first time
	update_code();

	if (timeout > 0) {
		add_new_timer(timers, update_code , timeout);
	}
}

//==============================================================================
//IE BUG ON XML
//==============================================================================

jQuery.parseXml = function(xml)
{
        if (jQuery.browser.msie)
        {
                var xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
                xmlDoc.loadXML(xml);
                return xmlDoc;
        }

        return xml;
};

// ============================================================================
// OTHER
// ============================================================================

jQuery.showMail = function(string)
{
        reg = /^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i;
};

jQuery.timeToHuman =  function (time)
{
        var theDate = new Date(time * 1000);
        return theDate.toUTCString();
};

jQuery.timestamp_to_smart_format = function(timestamp)
{
	var n = new Date();

	var t = new Date( parseInt(timestamp) *1000 );

	if ((n.getDate() == t.getDate()) && (n.getMonth() == t.getMonth()) && (n.getFullYear() == t.getFullYear())) {

		var h   = t.getHours();
		var min = t.getMinutes();
		var s   = t.getSeconds();
		return  ((h<=9)? '0'+h:h) +":"+ ((min<=9)? '0'+min:min) +":" + ((s<=9)? '0'+s:s);
	}
	else {
		var y   = t.getFullYear();
		var m   = t.getMonth() + 1;
		var d   = t.getDate();
		var h   = t.getHours();
		var min = t.getMinutes();
		var s   = t.getSeconds();
		return  y +"-"+  ((m<=9)? '0'+m:m)  +"-"+ ((d<=9)? '0'+d:d) +" "+ ((h<=9)? '0'+h:h) +":"+ ((min<=9)? '0'+min:min) +":" + ((s<=9)? '0'+s:s);

	}


}

jQuery.timestamp_to_iso = function(timestamp)
{
	var t = new Date( parseInt(timestamp) *1000 );
	var y   = t.getFullYear();
	var m   = t.getMonth() + 1;
	var d   = t.getDate();
	var h   = t.getHours();
	var min = t.getMinutes();
	var s   = t.getSeconds();
	return  y +"-"+  ((m<=9)? '0'+m:m)  +"-"+ ((d<=9)? '0'+d:d) +" "+ ((h<=9)? '0'+h:h) +":"+ ((min<=9)? '0'+min:min) +":" + ((s<=9)? '0'+s:s);
}

jQuery.timestamp_to_iso_short = function(timestamp)
{
	var t = new Date( parseInt(timestamp) *1000 );
	var y   = t.getFullYear();
	var m   = t.getMonth() + 1;
	var d   = t.getDate();
	return  y +"-"+  ((m<=9)? '0'+m:m)  +"-"+ ((d<=9)? '0'+d:d);
}


// ============================================================================
// DEFAULT DIALOGS
// ============================================================================

function ask_confirm(msg, confirm_callback, cancel_callback)
{
	ret = confirm(msg);
	if (ret)
		confirm_callback();
	else
		cancel_callback();
}


// ============================================================================
// SANET UTILS
// ============================================================================

function status_to_str(status)
{
	return status==10 ? 'DN':
	       status==20 ? 'FA':
	       status==30 ? 'UD':
	       status==40 ? 'UU':
	       status==50 ? 'TD':
	       status==60 ? 'TU':
	       status==70 ? 'IN':
	       status==100 ? 'UP': '';
}

jQuery.timestamp_to_iso = function(timestamp)
{
	var t = new Date( parseInt(timestamp) *1000 );
	var y   = t.getFullYear();
	var m   = t.getMonth() + 1;
	var d   = t.getDate();
	var h   = t.getHours();
	var min = t.getMinutes();
	var s   = t.getSeconds();
	return  y +"-"+  ((m<=9)? '0'+m:m)  +"-"+ ((d<=9)? '0'+d:d) +" "+ ((h<=9)? '0'+h:h) +":"+ ((min<=9)? '0'+min:min) +":" + ((s<=9)? '0'+s:s);
}

jQuery.timestamp_to_iso_short = function(timestamp)
{
	var t = new Date( parseInt(timestamp) *1000 );
	var y   = t.getFullYear();
	var m   = t.getMonth() + 1;
	var d   = t.getDate();
	return  y +"-"+  ((m<=9)? '0'+m:m)  +"-"+ ((d<=9)? '0'+d:d);
}




// Original JavaScript code by Chirp Internet: www.chirp.com.au
// Please acknowledge use of this code by including this header.
function checkTime(v)
{
	var r = "";
	var h;
	var m='00';
	var s='00';

	// regular expression to match required time format
	re = /^(\d{1,2})(?:\:(\d{2})(?:\:(\d{2}))?)?$/;

	if (v != '') {
		if ((regs = v.match(re))) {

			// 24-hour time format
			if (regs[1] > 23)
				return ""
			else
				h = regs[1];

			if (regs[2])
			if (regs[2] < 0 || 59 < regs[2])
				return ""
			else
				m = regs[2];

			if (regs[3])
			if (regs[3] < 0 || 59 < regs[3])
				return ""
			else
				s = regs[3];

			r = h+':'+m+':'+s;
		}
	}

	return r;
}



(function($) {
	/*
	 * <div id="tree" url="http://127.0.0.1:8000/sanet/rest/node/20/">
	 * 	*** ROOT TREE ***
	 * 	<div class="content">
	 * 	<ul>
	 * 			*** TREE ELEMENT ***
	 * 			<li class="tree-element" sanet_urn="container/17" name="container/17">
	 * 				<span class="treexpansion xpanded collaps" url="http://127.0.0.1:8000/sanet/rest/container/17/"/>
	 * 				<span id="container-17" class="resource inline container" sanet_urn="container/17" type="container">
	 * 				</span>
	 * 				
	 * 				<div class="content" style="display: block;">
	 *                              <ul>
	 * 						... SUB TREE ...
	 *                              </ul>
	 * 				</div>
	 * 			</li>
	 * 			...
	 * 			...
	 * 	</ul>
	 * 	</div>
	 * </div>
	 */
	
	var TREE_TEMPLATE = '\
	<li name="@@resource_type@@/@@id@@" class="tree-element" sanet_urn="@@sanet_urn@@"> \
		<span class="@@xpand_class@@ treexpansion"></span>\
		\
		<span \
		      class="resource inline @@resource_type@@"\
		      id="@@resource_type@@-@@id@@"\
		      type="@@resource_type@@" \
		      sanet_urn="@@sanet_urn@@"\
		      @@style@@ >\
			<a class="ctx_enabled drop_element"  \
			   sanet_urn="@@sanet_urn@@" \
			   href="#rest/@@resource_type@@/@@id@@/">@@resource@@</a> \
		</span> \
		\
		@@subtree@@ \
	</li>\
	';		
	
	/*-------------------------------------------------------------------*/
	/* TEMPLATE FUNCTIONS                                                */
	/*-------------------------------------------------------------------*/
	
	function create_full_html_tree(treedata)
	{
		var html = "<div class='content'>";
		html += '<ul>';
		for (var i=0; i< treedata.length; i++) {
			var e = treedata[i];
			html += create_html_tree_node(e);
		}
		html +='</ul>';		
		html +='</div>';
		return html;	
	}	
	
	function create_html_tree_node(e)
	{
		
		var t = TREE_TEMPLATE;
		t = t.replace(/@@sanet_urn@@/g    , e.sanet_urn);
		t = t.replace(/@@resource@@/g     , e.text     );
		t = t.replace(/@@resource_type@@/g, e.type     );
		t = t.replace(/@@id@@/g           , e.id       );
		
		var style = '';
		if (e.icon != undefined) {
			if (e.type != e.icon) {
				var icon_url = '/static/theme/img/resources/'+e.icon+'16x16.png';
				style = "style='background:transparent url("+icon_url+") no-repeat scroll left center;'"
			}
		}
		

		t = t.replace(/@@style@@/g           , style       );
		
		
		
		html_subtree = '';
		xpand_class  = 'xpand';
		if (e.subtree != undefined) {
			html_subtree = create_full_html_tree(e.subtree);
			xpand_class = 'xpanded collaps';
		}
		t = t.replace(/@@subtree@@/g      , html_subtree);
		t = t.replace(/@@xpand_class@@/g  , xpand_class );		
		return t;
	}		
	
	/*-------------------------------------------------------------------*/
	/* EVENTS                                                            */
	/*-------------------------------------------------------------------*/	
	
	$('span.collaps').live('click',function(){
		$(this).siblings('.content').toggle();
		$(this).addClass('xpand');
		$(this).removeClass('collaps');
	});

	$('span.xpand').live('click',function(){
		
		if($(this).hasClass('xpanded')){
			$(this).siblings('.content').toggle();
			$(this).addClass('collaps');
			$(this).removeClass('xpand');
		}
		else{
			$(this).addClass('collaps');
			$(this).addClass('xpanded');
			$(this).removeClass('xpand');

			var element   = $(this).siblings('span')[0];
			var sanet_urn = $(element).attr('sanet_urn');

			$(this).labsTree(jQuery.pre, 'rest/' + sanet_urn+'/');
			$(this).loadSubTree();
		}
	});

	/*-------------------------------------------------------------------*/
	/* COSTRUCTOR                                                        */
	/*-------------------------------------------------------------------*/	

	$.fn.labsTree = function(base,res){

		var url = base+res;
		$(this).attr('url', url);
	}

	/*-------------------------------------------------------------------*/
	/* METHODS                                                           */
	/*-------------------------------------------------------------------*/	
	
	$.fn.loadTreeToResource = function(callback)
	{

		var url = $(this).attr('url');
		
		var path = url+"subtreepath/";
		
		var ROOT = $(this);

		$.ajax({
			type: 'GET',
			url: path,
			dataType:'plain/text',
			complete: function(r, s){
				if (s == "success") {
					var json_string   = r.responseText;
					
					var treedata       = $.JSON.parse(json_string);
					
					_update_tree_dom(ROOT, treedata);

					jQuery.post_load_handler();	
					
					if (callback != undefined) 
						callback();
				}
			}
		});
	};	
	
	/*-------------------------------------------------------------------*/
	
	$.fn.loadSubTree = function()
	{

		url = $(this).attr('url');
		var path = url+"subtree/";
		
		var ROOT = $(this).parent();

		if($(this).siblings('ul').length ==0){

			$.ajax({
				dataType:'plain/text',
				url:path,
				type:'GET',
				complete: function(r, s){
					if (s == "success") {
						var json_string   = r.responseText;
						
						var msgdata       = $.JSON.parse(json_string);
						
						var html = create_full_html_tree(msgdata);
						ROOT.append(html);
						
						jQuery.post_load_handler();	
					}
				}
			});
		}
	};
	
	$.fn.reload = function() 
	{
		$(this).loadSubTree();
	};
	
	/*-------------------------------------------------------------------*/
	
	var level = 0;
	function repeat(s, n) { var r=""; for (var a=0;a<n;a++) r+=s; return r;}

	
	function _update_tree_dom(dom_tree_element, treedata)
	{
		//console.log( repeat('--',level) + dom_tree_element.attr('name') + dom_tree_element.attr('class'));
		
		level +=1;

		// Find the DOM content of the current tree node
		var tree_content = $(dom_tree_element).children('.content');
		
		// No content?
		if (tree_content.size() == 0) {
			//console.log( repeat('  ',level) + 'DOM empty');
			//
			// This is simple
			//
			// Compose the content as plain HTML text and show it.
			var html_content = create_full_html_tree(treedata);
			
			dom_tree_element.append(html_content);
		}
		else {
			//console.log( repeat('  ',level) + 'DOM with nodes');
			//
			// This is complex.
			//
			// we must update the existing the content of this DOM tree 
			// with new data from 'treedata'.
			var ul_tree_element =  $(tree_content[0]).children('ul')[0];
			
			__update_dom_tree_element( $(ul_tree_element), treedata );
			
			// We are here because we updated this tree and
			// we want to show it opened. Check visibility.
			if ($(tree_content[0]).is(':visible') == false) {
				$(tree_content[0]).toggle();
			}
		}
		
		level -= 1;
	}
	
	//function update_dom_tree_element( tree_list_element, treedata )
	//{ 
	//	var tree_nodes = tree_list_element.children('li');
	//
	function __update_dom_tree_element( ul_element, treedata )
	{
		var tree_nodes = ul_element.children('li');

		var i;
		var valid_nodes = new Array();
		for (i=0; i < treedata.length; i++) 
			valid_nodes.push( treedata[i].sanet_urn );
		
		//
		// Removing old elements from the DOM
		//
		tree_nodes.each( function() {
			var node_element = $(this);
			
			var sanet_urn = node_element.attr('sanet_urn');
			
			var notfound = $.inArray(sanet_urn, valid_nodes) < 0;
			
			if (notfound) {
				//alert("Old node " + sanet_urn + " to remove from gui");
				$(this).remove();
			}
		});		
		
		//
		// Update existing nodes
		//
		//alert("Updating existing nodes");
		
		var previous_node = undefined;
		
		for (var i=0; i < treedata.length; i++) {
			
			var node_data    = treedata[i];
			
			var node_elements = ul_element.find("li[name='"+ node_data.sanet_urn + "']");
			
			//console.log( repeat('--',level) + node_data.sanet_urn + ' ' + node_data.text ) ;
			//console.log( repeat('  ',level) + 'in DOM: '+(node_elements.size() != 0)+')' );

			//alert(node_data.sanet_urn + " in DOM = " + node_elements.size());
			
			// tree node already in the DOM
			if (node_elements.size() != 0) {

				var node_element = $(node_elements[0]);
				
				//console.log( repeat('  ',level) +'  element sanet_urn='+ node_element.attr('sanet_urn')) ;
				//console.log( repeat('  ',level) +'  subtree = ' + (node_data.subtree != undefined) );

				// We have data about the subtree of this node
				// Update the DOM subtree too!
				if (node_data.subtree != undefined) {
					
					_update_tree_dom(node_element, node_data.subtree);
					
					//console.log( repeat('  ',level) +'  fixing button****');
					
					// Fix CSS classes in order to expand the element
					var button = node_element.children('span.xpand:first-child')[0];
					$(button).addClass('collaps');
					$(button).addClass('xpanded');
					$(button).removeClass('xpand');				
				}
				
				previous_node = node_element;
				
			}
			// The DOM does not contain an element, add it
			else {
				var html_new_node = create_html_tree_node(node_data);
				
				// This is the first element?
				if (previous_node == undefined) {
					$(html_new_node).prepend( ul_element ); // Add first inside the <ul>
				}
				else {
					$(html_new_node).insertAfter(previous_node); // Add after the previous element
				}
			}
			
		}
		
		/*	
		var ul_element = $( $(tree_content[0]).children('ul')[0] );
		var tree_nodes = ul_element.children('li');
		
		
		var i = 0;
		var j = 0;
		
		while ((i < tree_nodes.size()) && ( j < treedata.length )) {

			var node_element = $(tree_nodes[i]);
			var node_data    = treedata[j];
			
			var r = __compare_tree_ids(node_element.attr('sanet_urn'), node_data.sanet_urn);
			
			alert( "Comparing: " + node_element.attr('sanet_urn') + ' ' + node_data.sanet_urn + ' = ' + r);
			
			// Same element
			if (r == 0) {
				
				// If the data contains a subtree we should expand
				// visible tree
				if (node_data.subtree != undefined) {
					alert("Updating subtree for " + node_element.attr('sanet_urn'));
					fill_tree(node_element, node_data.subtree);
					
					// Fix CSS classes in order to expand the element
					var button = $('span.xpand:first-child', node_element)
					button.addClass('collaps');
					button.addClass('xpanded');
					button.removeClass('xpand');				
				}


				// Move to next nodes				
				i++;
				j++;	
			}
			// The DOM does not contain an element, add it
			else if (r > 0) {
				var html_new_node = create_html_tree_node(node_data);
				$(html_new_node).insertBefore( node_element );
				
				i++; // adjust index of current tree element after the insert
				j++; // move to the next data element
			}
			// The DOM contains a element no more valid, remove it
			else {	
				nodes_to_remove.append(node_element);
				i++;	
			}
		}

		// Finish DOM nodes
		for (; j < treedata.length; j++) {
			var node_data    = treedata[j];
		}
		*/
	}
	
	/*
	function __compare_tree_ids( id1, id2 )
	{
		var p = id1.split('/'); var rtype1 = p[0]; var rid1 = p[1];
		var p = id2.split('/'); var rtype2 = p[0]; var rid2 = p[1];
		
		var values = Array();
		values['container'] = 5;
		values['node'     ] = 4;
		values['iface'    ] = 3;
		values['target'   ] = 2;
		values['measure'  ] = 1;
		
		if (rtype1 == rtype2) {
			return (parseInt(rid1) - parseInt(rid2));
		}
		else {
			return (values[ rtype1 ] - values[ rtype2 ]);
		}
	}
	*/
	
})(jQuery);
//------------------------------------------------------------------------------//
//                                                                              //
//------------------------------------------------------------------------------//

jQuery.UIBlockOrderInsolute = jQuery.UIBlock.extend({

    action_handler : function(action_el) {
        if (action_el.attr('name') == "new_note") {
            return this.open_new_note_form(action_el.attr('url'));
        } else {
            return this._super(action_el);
        }
    },

    render_actions : function(data) {
        return ""
    },

    render_content : function(data) {

        function capitalize_str(s) {
            c = s.substring(0,1).toUpperCase();
            s = c + s.substring(1, s.length);
            return s;
        }
        
        BLOCK_ELEMENT = jQuery.parseXml(data);

        //code
        jQel = jQuery(BLOCK_ELEMENT);
        
        if (jQel.children('error').length != 0)
            return jQel.text()
        
        //template elements
        var content_template = '\
        <div>\
            <form id="insolute_id" method="POST" action="@@action_url@@">\
            <div class="list_actions">@@list_actions@@</div> \
            @@content@@\
            </form>\
        </div>\
        '

        //Render block actions
        var contents = jQel.find('content[type="user_actions"]');

        var action_template = "<input type='submit' href=\"#\" name=\"@@action_name@@\" value=\"@@action_verbose_name@@\" />";
        var actions = '';

        var form_url = "";
        if (contents.find('action').length > 0) {
        
            contents.find('action').each(function(){
                var action = action_template.replace(/@@action_name@@/g, $(this).attr("name"));
                action = action.replace(/@@action_verbose_name@@/g, $(this).attr("verbose_name"));
                form_url = $(this).attr("url");
                actions += action;
            });
        }

        content_template = content_template.replace(/@@list_actions@@/g, actions);
        content_template = content_template.replace(/@@action_url@@/g, form_url);
            

        var form_content = jQel.find('content[type="table"]').html();
        content_template = content_template.replace(/@@content@@/g, form_content);
        
        return content_template;
        
    },


    post_load_handler : function() {
        var form_el = $("#insolute_id");
        form_el.ajaxForm({
            dataType : 'xml',
            success : function(responseXML, statusText, xhr, $form)  {
            if (xhr.responseText.match('class="errorlist"')) {
                form_html = $(xhr.responseText).find('tbody');
                form_el.find('tbody').html(form_html.html());
            } else 
                window.location.reload();
            }
        });
        this._super();
    },

    //------------------------------------------------------------------------------//
    //                                                                              //
    //------------------------------------------------------------------------------//


})

jQuery.BLOCKS["order_insolute"] = new jQuery.UIBlockOrderInsolute("order_insolute");


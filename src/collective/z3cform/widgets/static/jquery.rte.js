/*
* jQuery RTE plugin 0.5.1 - create a rich text form for Mozilla, Opera, Safari and Internet Explorer
*
* Copyright (c) 2009 Batiste Bieler
* Distributed under the GPL Licenses.
* Distributed under the MIT License.
*/

// define the rte light plugin
(function($) {

if(typeof $.fn.rte === "undefined") {

    var defaults = {
        media_url: "",
        content_css_url: "rte.css",
        dot_net_button_class: null,
        max_height: 350,
        iframe_height: 100,
        format_block: true,
        bold: true,
        italic: true,
        unordered_list: true,
        link:true,
        image:true,
        allow_disable:true
    };

    $.fn.rte = function(options) {

    $.fn.rte.html = function(iframe) {
        return iframe.contentWindow.document.getElementsByTagName("body")[0].innerHTML;
    };

    // build main options before element iteration
    var opts = $.extend(defaults, options);

    // iterate and construct the RTEs
    return this.each( function() {
        var textarea = $(this);
        var iframe;
        var element_id = textarea.attr("id");

        // enable design mode
        function enableDesignMode() {

            var content = textarea.val();

            // Mozilla needs this to display caret
            if($.trim(content)=='') {
                content = '<br />';
            }

            // already created? show/hide
            if(iframe) {
                console.log("already created");
                textarea.hide();
                $(iframe).contents().find("body").html(content);
                $(iframe).show();
                $("#toolbar-" + element_id).remove();
                textarea.before(toolbar());
                return true;
            }

            // for compatibility reasons, need to be created this way
            iframe = document.createElement("iframe");
            iframe.frameBorder=0;
            iframe.frameMargin=0;
            iframe.framePadding=0;
            iframe.height=opts.iframe_height;
            if(textarea.attr('class'))
                iframe.className = textarea.attr('class');
            if(textarea.attr('id'))
                iframe.id = element_id;
            if(textarea.attr('name'))
                iframe.title = textarea.attr('name');

            textarea.after(iframe);

            var css = "";
            if(opts.content_css_url) {
                css = "<link type='text/css' rel='stylesheet' href='" + opts.content_css_url + "' />";
            }

            var doc = "<html><head>"+css+"</head><body class='frameBody'>"+content+"</body></html>";
            tryEnableDesignMode(doc, function() {
                $("#toolbar-" + element_id).remove();
                textarea.before(toolbar());
                // hide textarea
                textarea.hide();

            });

        }

        function tryEnableDesignMode(doc, callback) {
            if(!iframe) { return false; }

            try {
                iframe.contentWindow.document.open();
                iframe.contentWindow.document.write(doc);
                iframe.contentWindow.document.close();
            } catch(error) {
                //console.log(error);
            }
            if (document.contentEditable) {
                iframe.contentWindow.document.designMode = "On";
                callback();
                return true;
            }
            else if (document.designMode != null) {
                try {
                    iframe.contentWindow.document.designMode = "on";
                    callback();
                    return true;
                } catch (error) {
                    //console.log(error);
                }
            }
            setTimeout(function(){tryEnableDesignMode(doc, callback)}, 500);
            return false;
        }

        function disableDesignMode(submit) {
            var content = $(iframe).contents().find("body").html();

            if($(iframe).is(":visible")) {
                textarea.val(content);
            }

            if(submit !== true) {
                textarea.show();
                $(iframe).hide();
            }
        }

        // create toolbar and bind events to it's elements
        function toolbar() {
            var tb = $("<div class='rte-toolbar' id='toolbar-"+ element_id +"'></div>");
            var internal_div = $("<div></div>");

            if (opts.format_block){
                var format_block = $("<p>\
                                        <select>\
                                            <option value=''>Block style</option>\
                                            <option value='p'>Paragraph</option>\
                                            <option value='h3'>Title</option>\
                                            <option value='address'>Address</option>\
                                        </select>\
                                     </p>");

                $('select', format_block).change(function(){
                    var index = this.selectedIndex;
                    if( index!=0 ) {
                        var selected = this.options[index].value;
                        formatText("formatblock", '<'+selected+'>');
                    }
                });

                internal_div.append(format_block);

                var iframeDoc = $(iframe.contentWindow.document);

                var select = $('select', internal_div)[0];
                iframeDoc.mouseup(function(){
                    setSelectedType(getSelectionElement(), select);
                    return true;
                });

                iframeDoc.keyup(function() {
                    setSelectedType(getSelectionElement(), select);
                    var body = $('body', iframeDoc);
                    if(body.scrollTop() > 0) {
                        var iframe_height = parseInt(iframe.style['height'])
                        if(isNaN(iframe_height))
                            iframe_height = 0;
                        var h = Math.min(opts.max_height, iframe_height+body.scrollTop()) + 'px';
                        iframe.style['height'] = h;
                    }
                    return true;
                });

            }

            if (opts.bold || opts.italic){
                var style_paragraph = $("<p></p>");
                if (opts.bold){
                    var bold = $("<a href='#' class='bold'><img src='"+opts.media_url+"bold.gif' alt='bold' /></a>");
                    style_paragraph.append(bold);
                    $('.bold', style_paragraph).click(function(){ formatText('bold');return false; });
                }
                if (opts.italic){
                    var italic = $("<a href='#' class='italic'><img src='"+opts.media_url+"italic.gif' alt='italic' /></a>");
                    style_paragraph.append(italic);
                    $('.italic', style_paragraph).click(function(){ formatText('italic');return false; });
                }

                internal_div.append(style_paragraph);
            }

            if (opts.unordered_list || opts.link || opts.image || opts.allow_disable){
                var extras_paragraph = $("<p></p>");
                if (opts.unordered_list){
                    var ulist = $("<a href='#' class='unorderedlist'><img src='"+opts.media_url+"unordered.gif' alt='unordered list' /></a>");
                    extras_paragraph.append(ulist);
                    $('.unorderedlist', extras_paragraph).click(function(){ formatText('insertunorderedlist');return false; });
                }
                if (opts.link){
                    var link = $("<a href='#' class='link'><img src='"+opts.media_url+"link.png' alt='link' /></a>");
                    extras_paragraph.append(link);
                    $('.link', extras_paragraph).click(function(){
                        var p=prompt("URL:");
                        if(p)
                            formatText('CreateLink', p);
                        return false; });
                }
                if (opts.image){
                    var image = $("<a href='#' class='image'><img src='"+opts.media_url+"image.png' alt='image' /></a>");
                    extras_paragraph.append(image);
                    $('.image', extras_paragraph).click(function(){
                        var p=prompt("image URL:");
                        if(p)
                            formatText('InsertImage', p);
                        return false; });
                }
                if (opts.allow_disable){
                    var allow_disable = $("<a href='#' class='disable'><img src='"+opts.media_url+"close.gif' alt='close rte' /></a>");
                    extras_paragraph.append(allow_disable);
                    $('.disable', extras_paragraph).click(function() {
                        disableDesignMode();
                        var edm = $('<a class="rte-edm" href="#">Enable design mode</a>');
                        tb.empty().append(edm);
                        edm.click(function(e){
                            e.preventDefault();
                            enableDesignMode();
                            // remove, for good measure
                            $(this).remove();
                        });
                        return false;
                    });

                }

                internal_div.append(extras_paragraph);

            }

            tb.append(internal_div);

            // .NET compatability
            if(opts.dot_net_button_class) {
                var dot_net_button = $(iframe).parents('form').find(opts.dot_net_button_class);
                dot_net_button.click(function() {
                    disableDesignMode(true);
                });
            // Regular forms
            } else {
                $(iframe).parents('form').submit(function(){
                    disableDesignMode(true);
                });
            }


            return tb;
        };

        function formatText(command, option) {
            iframe.contentWindow.focus();
            try{
                iframe.contentWindow.document.execCommand(command, false, option);
            }catch(e){
                //console.log(e)
            }
            iframe.contentWindow.focus();
        };

        function setSelectedType(node, select) {
            while(node.parentNode) {
                var nName = node.nodeName.toLowerCase();
                for(var i=0;i<select.options.length;i++) {
                    if(nName==select.options[i].value){
                        select.selectedIndex=i;
                        return true;
                    }
                }
                node = node.parentNode;
            }
            select.selectedIndex=0;
            return true;
        };

        function getSelectionElement() {
            if (iframe.contentWindow.document.selection) {
                // IE selections
                selection = iframe.contentWindow.document.selection;
                range = selection.createRange();
                try {
                    node = range.parentElement();
                }
                catch (e) {
                    return false;
                }
            } else {
                // Mozilla selections
                try {
                    selection = iframe.contentWindow.getSelection();
                    range = selection.getRangeAt(0);
                }
                catch(e){
                    return false;
                }
                node = range.commonAncestorContainer;
            }
            return node;
        };
        
        // enable design mode now
        enableDesignMode();

    }); //return this.each
    
    }; // rte

} // if

})(jQuery);

function init_rte() {
    $.each($(".rte-widget"), function(){
        var $this = $(this);
        $(this).rte({
            content_css_url: "++resource++collective.z3cform.widgets/rte.css",
            media_url: "++resource++collective.z3cform.widgets/rte/",
            iframe_height: $this.data('iframe_height'),
            format_block: $this.data('format_block'),
            bold: $this.data('bold'),
            italic: $this.data('italic'),
            unordered_list: $this.data('unordered_list'),
            link: $this.data('link'),
            image: $this.data('image'),
            allow_disable: $this.data('allow_disable')
        });
    });
}

$(document).ready(function(){
    init_rte();
});
// This is based on jQueryFileTree by   Cory S.N. LaViska

function formwidget_autocomplete_new_value(input_box,value,label) {
    (function($) {
        var base_id = input_box[0].id.replace(/-widgets-query$/,"");
        var base_name = input_box[0].name.replace(/\.widgets\.query$/,"");
        var widget_base = $('#'+base_id+"-input-fields");

        var all_fields = widget_base.find('input:radio, input:checkbox');

        // Clear query box and uncheck any radio boxes
        input_box.val("");
        widget_base.find('input:radio').attr('checked', '');

        // If a radio/check box for this value already exists, check it.
        var selected_field = widget_base.find('input[value="' + value + '"]');
        if(selected_field.length) {
            selected_field.each(function() { this.checked = true; });
            return;
        }

        widget_base, base_name, base_id
        // Create the box for this value
        var idx = all_fields.length;
        var klass = widget_base.data('klass');
        var title = widget_base.data('title');
        var type = widget_base.data('input_type');
        var span = $('<span/>').attr("id",base_id+"-"+idx+"-wrapper").attr("class","option");
        // Note that Internet Explorer will usually *not* let you set the name via setAttribute.
        // Also, setting the type after adding a input to the DOM is also not allowed.
        // Last but not least, the checked attribute doesn't always behave in a way you'd expect
        // so we generate this one as text as well.
        span.append($("<label/>").attr("for",base_id+"-"+idx)
                                 .append($('<input type="' + type + '"' +
                                                ' name="' + base_name + ':list"' +
                                                ' checked="checked" />')
                                            .attr("id",base_id+"-"+idx)
                                            .attr("title",title)
                                            .attr("value",value)
                                            .addClass(klass)
                                        )
                                 .append(" ")
                                 .append($("<span>").attr("class","label").text(label))
                                 );
        widget_base.append(span);
    }(jQuery));
}

if(jQuery) (function($){
    $.extend($.fn, {
        contentTreeAddRelated: function() {
                    var contenttree_window = (this).parents(".contenttreeWindow");
                    var input_box = $('#'+ contenttree_window[0].id.replace(/-contenttree-window$/,"-widgets-query"));
                    var base_id = input_box[0].id.replace(/-widgets-query$/,"");
                    var base_name = input_box[0].name.replace(/\.widgets\.query$/,"");
                    var widget_base = $('#'+base_id+"-input-fields");
                    var all_fields = widget_base.find('span');
                    all_fields.remove()
                    contenttree_window.find('.relatedWidget ul.recieve .navTreeItem > a').each(function () {
                        formwidget_autocomplete_new_value(input_box,$(this).attr('href'),$.trim($(this).text()));
                    });

                    $(this).contentTreeCancel();
                }});
})(jQuery);

(function ($) {
   $.fn.liveDraggable = function (opts) {
      this.live("mouseover", function() {
         if (!$(this).data("init")) {
            $(this).data("init", true).draggable(opts);
         }
      });
      return $();
   };
}(jQuery));


function relatedWidgetSearchFilter(url) {
  var queryVal = $("#relatedWidget-search-input").val();
  $.ajax({
    url: url,
    data: {'q':queryVal},
    success: function(info){
      $(".relatedWidget ul.from").html(info);
      return false;
    }
  });
  return false;
}

$(function() {
		$( ".relatedWidget ul.from .navTreeItem").liveDraggable({ containment: ".relatedWidget",  scroll: false, helper: "clone"}); 
	  $(".relatedWidget ul.recieve").droppable({
        			activeClass: "ui-state-default",
        			hoverClass: "ui-state-hover",
        			drop: function(event, ui) {        			  
        			  var children = $(this).children();
        			  var i = 0;
        			  var exists = false;
        			  for(i=0; i<children.length; i++) {
        			    if(ui.draggable.attr('uid') == $(children[i]).attr('uid')){
        			      exists = true;
        			    }
        			  }
        			  if(!exists) {
        			    var clon = ui.draggable.clone()
        			    var children = $("ul",clon);
        			    if(children.length) {
        			      children.remove();
        			    }
        			    clon.append("<div class='related-item-close'>X</div>");
        			    clon.appendTo( this );
        			  }	
        			}
        		}).sortable();
    $(".relatedWidget ul.recieve li").append("<div class='related-item-close'>X</div>");
    $(".relatedWidget ul.recieve li a").live("click", function(e) {
      e.preventDefault();
      return false;
    })
    $(".related-item-close").live("click", function() {
        $(this).parent().remove();
    })

});
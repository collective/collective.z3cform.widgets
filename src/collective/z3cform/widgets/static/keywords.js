(function ( $ ) {
    var filters = $.expr[":"];
    if ( !filters.focus ) { 
        filters.focus = function( elem ) {
           return elem === document.activeElement && ( elem.type || elem.href );
        };
    }
})( jQuery );


function keywordTokenInputActivate(id, newValues, oldValues) {
  $('#'+id).tokenInput(newValues, {
      theme: "facebook",
      tokenDelimiter: "\n",
      tokenValue: "name",
      preventDuplicates: true,
      prePopulate: oldValues
  });

  $("#token-input-"+id).change(function(){
    var value = $(this).val();
    $("#"+id).tokenInput("add", {id: value, name: value});
  })
  
  $(document).keypress(function(e) {
      if(e.keyCode == 13) {
        if($("#token-input-"+id).is(":focus")) {
          e.preventDefault();
          var value = $("#token-input-"+id).val();
          $("#"+id).tokenInput("add", {id: value, name: value});
          return false;
        }
      }
  });
}
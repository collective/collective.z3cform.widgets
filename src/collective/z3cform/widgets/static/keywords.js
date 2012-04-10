function keywordTokenInputActivate(id, newValues, oldValues) {
  $('#'+id).tokenInput(newValues, {
      theme: "facebook",
      tokenDelimiter: "\n",
      tokenValue: "name",
      preventDuplicates: true,
      prePopulate: oldValues
  });
  $("#token-input-"+id).change(function(){
    var value = $(this).val()
    $("#"+id).tokenInput("add", {id: value, name: value});
  })
}
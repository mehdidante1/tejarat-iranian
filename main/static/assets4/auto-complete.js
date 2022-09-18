$(document).ready(function(){

    //delete item from cart

    $(function() {
        $("#query").autocomplete({
          source: "/search-auto",
          select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
          },
          minLength: 2,
        });
      });
    
      function AutoCompleteSelectHandler(event, ui)
      {
        var selectedObj = ui.item;
      }
    //end
});


$( document ).ready(function() {  
  $('textarea').autogrow({onInitialize: true});
  
  // Add Form
  $('#add_form').click(function() {
    var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('.project-cards').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    var forms = $('.project-cards').find("div:visible").length;
    console.log(forms);
    if (forms > 4) $('#add_form').attr('style', 'display:none');
  });

  // Remove Form
  $(".project-cards").on("click", "#remove_form", function(){
    var parent = $(this).parent("div");
    var index = parent.find("input:first").attr("id")[8]
    $('#id_form-' + index + '-DELETE').prop('checked', true);
    // var index = parent.find("input:first").attr("id")[8]
    // parent.append('<input type="checkbox" name="form-' + index + '-DELETE" id="id_form-' + index + '-DELETE" checked>')
    parent.attr("style", "display:none");
    forms = parent.length; 
    if (forms < 4) $('#add_form').attr('style', 'display:inline-block');
  });

  // Adds class to selected item
  $(".circle--pill--list a").click(function() {
    $(".circle--pill--list a").removeClass("selected");
    $(this).addClass("selected");
  });

  // Adds class to parent div of select menu
  $(".circle--select select").focus(function(){
   $(this).parent().addClass("focus");
   }).blur(function(){
     $(this).parent().removeClass("focus");
   });

  // Clickable table row
  $(".clickable-row").click(function() {
      var link = $(this).data("href");
      var target = $(this).data("target");

      if ($(this).attr("data-target")) {
        window.open(link, target);
      }
      else {
        window.open(link, "_self");
      }
  });

  // Clickable td
  $(".clickable-td").click(function() {
    var link = $(this).parent("tr").data("href");
    var target = $(this).parent("tr").data("target");

    if ($(this).attr("data-target")) {
      window.open(link, target);
    }
    else {
      window.open(link, "_self");
    }
});

  // Custom File Inputs
  var input = $(".circle--input--file");
  var text = input.data("text");
  var state = input.data("state");
  input.wrap(function() {
    return "<a class='button " + state + "'>" + text + "</div>";
  });
});
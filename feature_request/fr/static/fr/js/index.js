$(document).ready(function(){
  $('select').formSelect();
  $('.datepicker').datepicker({
    minDate : new Date()
  });
  $('.modal').modal();
  $('.collapsible').collapsible();
  $('.sidenav').sidenav();
  $('.title').characterCounter();

  $.validator.addMethod("regex", function(value, element, regex) {
    return regex.test(value);
  });

  $('form').each(function () {
    $(this).validate({
      rules: {
        title: {
          required: true,
          maxlength: 50,
          regex: /^\S/
        },
        description: {
          required: true,
          regex: /^\S/
        },
        client: "required",
        priority: "required",
        product: "required",
        targetDate: "required"
      },
      messages: {
        title: {
          required: "enter the title",
          maxlength: "title is too long",
          regex: "title cannot be blank"
        },
        description: {
          required: "enter the description",
          regex: "description cannot be blank"
        },
        client: {
          required: "choose the client"
        },
        priority: {
          required: "enter the client priority"
        },
        product: {
          required: "choose the product area"
        },
        targetDate: {
          required: "enter the target date"
        },
      },
      errorElement : 'div',
      errorPlacement: function(error, element) {
        var placement = $(element).data('error');
        if (placement) {
          $(placement).append(error);
        } else {
          error.insertAfter(element);
        }
      }
    });
  });

  $('.viewButton').click(function() {
    var requestId = $(this).data("edit");
    $.get("/" + requestId, function(data) {
      $('.card-title h4').text(data[0].fields.title);
      $('.card-content p').text(data[0].fields.description);
    });
  });

  var months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];


  function formatDate(date) {
	  return months[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear();
  }

  $('.editButton').click(function() {
    var requestId = $(this).data("edit");
    $.get("/" + requestId, function(data) {
      date = new Date(data[0].fields.targetDate);

      $('#editForm').attr('action', 'update/' + data[0].pk + '/');
      $("#title").val(data[0].fields.title);
      $("#description").val(data[0].fields.description);
      $("#client").val(data[0].fields.client);
      $("#priority").val(data[0].fields.priority);
      $("#product").val(data[0].fields.product);
      $("#targetDate").val(formatDate(date));
      M.updateTextFields();
    });
  });
});

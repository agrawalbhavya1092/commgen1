$( document ).ready(function() {
    $(".option-box").hide()
});

function toggleOptionBox(select){
    $(select.nextElementSibling).toggle();  
}

function toggleFillColor(obj) {
  // $("#custom-select-option-box").show();
  $(obj.parentElement.parentElement).show();
  if($(obj).prop('checked') == true) {
    $(obj).parent().css("background",'#c6e7ed');
  } else {
    $(obj).parent().css("background",'#FFF');
  }
}
// $(".custom-select-option").on("click", function() {
//   var checkboxObj = $(this).children("input");
//   $(checkboxObj).prop("checked",true);
//   toggleFillColor(checkboxObj);
// });
$("body").on("click",function(e){
  // if(e.target.id != "custom-select" && $(e.target).attr("class") != "custom-select-option") {
  if(!e.target.id.includes("custom-select") && $(e.target).attr("class") != "custom-select-option") {
    $("[id*='-option-box']").hide();
  }
});

$("#entity").change(function () {
  var entity = $(this).val();
  sendAjaxP1(entity)
});


function sendAjaxP1(entity){
          $.ajax({
        url: "/campaign/ajax/p1/",
        data: {
          'data': entity  
        },
        success: function (data) {
          // $("#custom-select-option-box").children().remove()
          $("#id_p1-option-box").html(data);
          $("#id_p2-option-box").children().remove()
          $("#id_m3-option-box").children().remove()
          $("#id_m4-option-box").children().remove()
          $("#id_m5-option-box").children().remove()
          $("#id_m6-option-box").children().remove()
        }
      });

}

function get_checked_checkboxes(checkbox_name){
  arr = []
        var oRadio = document.forms[3].elements[checkbox_name];
     for(var i = 0; i < oRadio.length; i++)
     {
        if(oRadio[i].checked)
        {
           arr.push(oRadio[i].value);
        }
     }
     return arr
}
$("#id_p1-option-box").change(function () {
  var p1 = []
  p1 = get_checked_checkboxes('p1[]')
  $.ajax({
    url: "/campaign/ajax/p2",
    data: {
      'data': p1
    },
    success: function (data) {
      $("#id_p2-option-box").html(data);
      $("#id_m3-option-box").children().remove()
      $("#id_m4-option-box").children().remove()
      $("#id_m5-option-box").children().remove()
      $("#id_m6-option-box").children().remove()
    }
  });
});
$("#id_p2-option-box").change(function () {
  var p2 = []
  p2 = get_checked_checkboxes('p2[]')

  $.ajax({
    url: "/campaign/ajax/m3/",
    data: {
      'data': p2
    },
    success: function (data) {
      $("#id_m3-option-box").html(data);
      $("#id_m4-option-box").children().remove()
      $("#id_m5-option-box").children().remove()
      $("#id_m6-option-box").children().remove()
    }
  });
});
$("#id_m3-option-box").change(function () {
  var m3 = []
  m3 = get_checked_checkboxes('m3[]')
  $.ajax({
    url: "/campaign/ajax/m4/",
    data: {
      'data': m3
    },
    success: function (data) {
      $("#id_m4-option-box").html(data);
      $("#id_m5-option-box").children().remove()
      $("#id_m6-option-box").children().remove()
    }
  });
});
$("#id_m4-option-box").change(function () {
  var m4 = []
  m4 = get_checked_checkboxes('m4[]')
  $.ajax({
    url: "/campaign/ajax/m5/",
    data: {
      'data': m4
    },
    success: function (data) {
      $("#id_m5-option-box").html(data);
      $("#id_m6-option-box").children().remove()
    }
  });
});
$("#id_m5-option-box").change(function () {
  var m5 = []
  m5 = get_checked_checkboxes('m5[]')

  $.ajax({
    url: "/campaign/ajax/m6",
    data: {
      'data': m5
    },
    success: function (data) {
      $("#id_m6-option-box").html(data);
    }
  });
});
$("#id_generic_company").change(function () {
  var generic_company = []
  generic_company = get_checked_checkboxes('generic_company[]');
  $.ajax({
  url: "/campaign/ajax/region/",
  data: {
    'data': generic_company
  },
  success: function (data) {
    $("#id_region-option-box").html(data);
  }
});
});
$("#id_region-option-box").change(function () {
var region = $(this).val();
$.ajax({
  url: "/campaign/ajax/country/",
  data: {
    'data': region
  },
  success: function (data) {
    $("#id_country").html(data);
  }
});
});
$("#id_country").change(function () {
var country = $(this).val();
$.ajax({
  url: "/campaign/ajax/location",
  data: {
    'data': country
  },
  success: function (data) {
    $("#id_location").html(data);
  }
});
});
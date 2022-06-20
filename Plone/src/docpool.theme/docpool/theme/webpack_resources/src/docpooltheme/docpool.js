require(["jquery", "jquery.marquee"], function ($) {
  "use strict";

  function loadDyn() {
    $("#mesz").load("refresh_time #time_table");
    $("section.portletRecent").load("refresh_recent #recent_content");
  }

  function getURLParam(name) {
    var regex = "[?&]" + name + "=([^&]*)";
    var query = location.search;
    if ((name = new RegExp(regex).exec(query))) return name[1];
  }

  var myDynTimer = setInterval(loadDyn, 60000);
  $(".documentByLine a").removeAttr("href").addClass("commentator");
  var type = $("#form-widgets-docType");
  if (type[0] != null && type[0].selectedIndex != null) {
    var dtParam = getURLParam("form.widgets.docType:list");
    if (typeof dtParam != "undefined") {
      type.val(dtParam);
    }
    var option = type[0].options[type[0].selectedIndex];
    var value = option.text;
    var title = $("h1.documentFirstHeading").text();
    $("h1.documentFirstHeading").text(title + " (" + value + ")");
  }

  $(document).ready(function () {
    $(".marquee").marquee({
      pauseOnHover: true,
      duration: 10000,
      //gap in pixels between the tickers
      gap: 50,
    });
  });
});

$(document).on("click", ".collapsible", function (event) {
  this.classList.toggle("active");
  var content = this.nextElementSibling;
  if (content.style.maxHeight) {
    content.style.maxHeight = null;
  } else {
    content.style.maxHeight = content.scrollHeight + "px";
  }
});

require(["jquery", "jquery.marquee"], function ($) {
  "use strict";

  function loadDyn() {
    $("#mesz").load("refresh_time #time_table");
    $("section.portletRecent").load("refresh_recent #recent_content");
  }

  var myDynTimer = setInterval(loadDyn, 60000);
  $(".documentByLine a").removeAttr("href").addClass("commentator");

  $(document).ready(function () {
    $(".marquee").marquee({
      pauseOnHover: true,
      duration: 10000,
      //gap in pixels between the tickers
      gap: 50,
    });
  });
});

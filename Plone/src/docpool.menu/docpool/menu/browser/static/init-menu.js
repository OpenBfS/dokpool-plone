define(["jquery", "docpool-menu-plugin"], function ($) {
  "use strict";

  jQuery(function ($) {
    var menu = $(".rm-nav").rMenu({
      minWidth: "768px",
      toggleBtnBool: false,
    });
  });
});

jQuery(function ($) {
  require(["docpool-menu"]);
});

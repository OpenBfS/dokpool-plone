// docpool.rei js/scss entry
import $ from "jquery";
import Registry from "@patternslib/patternslib/src/core/registry";

const isAnonymous = document.querySelector(".userrole-anonymous");
// Logged-In users
if (isAnonymous === null) {
  import("./styles.scss");
}

$(function () {
  if (typeof window.Faceted !== "undefined") {
    $(window.Faceted.Events).bind(window.Faceted.Events.AJAX_QUERY_SUCCESS, function () {
      // Async import the contentloader and do a mockup Registry scan
      Promise.all([import(/* webpackChunkName: "pat-contentloader-bfs" */ "./pat-contentloader-bfs")]).then((args) => {
        Registry.scan($("#content-core"));
      });
      // Open all metatitle
      $("#z3ctabel-toggles .z3ctable-toggle-metatitle").on("click", function (e) {
        var open_state_title = false;
        if ($(this).hasClass("state_open")) {
          open_state_title = true;
          $(this).removeClass("state_open");
        } else {
          open_state_title = false;
          $(this).addClass("state_open");
        }
        e.preventDefault();
        $("#faceted_table .metatitle").each(function () {
          // Its already open -> dont toggle
          if (!$(this).hasClass("close")) {
            $(this).click();
          }
        });
        if (open_state_title) {
          $("#faceted_table .metatitle").click();
        }
      });
      // Open all metainfos
      $("#z3ctabel-toggles .z3ctable-toggle-metadata").on("click", function (e) {
        var open_state_data = false;
        if ($(this).hasClass("state_open")) {
          open_state_data = true;
          $(this).removeClass("state_open");
        } else {
          open_state_data = false;
          $(this).addClass("state_open");
        }
        e.preventDefault();
        $("#faceted_table .metadata").each(function () {
          // Its already open -> dont toggle
          if (!$(this).hasClass("close")) {
            $(this).click();
          }
        });
        if (open_state_data) {
          $("#faceted_table .metadata").click();
        }
      });
    });
  }
});

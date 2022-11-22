import "@patternslib/patternslib/src/globals";
import { go_to } from "./window_functions";
import { makePopUp } from "./window_functions";
import registry from "@patternslib/patternslib/src/core/registry";
import jQuery from "jquery";

// Global functions needed in window
window.go_to = go_to;
window.makePopUp = makePopUp;

// Global styles
import("./docpool_styles/header-timetable.scss");

const isAnonymous = document.querySelector(".userrole-anonymous");
// Logged-In users
if (isAnonymous === null) {
  import("./theme.scss");
}

// Anonymous users
if (isAnonymous !== null) {
  import("./docpool_styles/anonymous.scss");
}

registry.init();

jQuery(document).ready(function (evt) {
  if (typeof Faceted !== "undefined") {
    $(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function () {
      // Async import the contentloader and do a mockup registry scan
      Promise.all([
        import(
          /* webpackChunkName: "pat-contentloader-bfs" */ "./docpool.rei/pat-contentloader-bfs"
        ),
      ]).then((args) => {
        registry.scan($("#content-core"));
      });
      // Open all metatitle
      $("#z3ctabel-toggles .z3ctable-toggle-metatitle").on(
        "click",
        function (e) {
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
        }
      );
      // Open all metainfos
      $("#z3ctabel-toggles .z3ctable-toggle-metadata").on(
        "click",
        function (e) {
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
        }
      );
    });
  }
});

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
    $(window.Faceted.Events).bind(
      window.Faceted.Events.AJAX_QUERY_SUCCESS,
      function () {
        // Async import the contentloader and do a mockup Registry scan
        Promise.all([
          import(
            /* webpackChunkName: "pat-contentloader-bfs" */ "./pat-contentloader-bfs"
          ),
        ]).then((args) => {
          Registry.scan($("#content-core"));
        });
        // Open all metatitle
        $("#z3ctabel-toggles .z3ctable-toggle-metatitle").on(
          "click",
          function (e) {
            var isOpen = $(this).hasClass("state_open");
            $(this).toggleClass("state_open");
            e.preventDefault();
            $("#faceted_table .metatitle.close").click();
            if (!isOpen) {
              $("#faceted_table .metatitle").click();
            }
          },
        );
        // Open all metainfos
        $("#z3ctabel-toggles .z3ctable-toggle-metadata").on(
          "click",
          function (e) {
            var isOpen = $(this).hasClass("state_open");
            $(this).toggleClass("state_open");
            e.preventDefault();
            $("#faceted_table .metadata.close").click();
            if (!isOpen) {
              $("#faceted_table .metadata").click();
            }
          },
        );
      },
    );
  }
});

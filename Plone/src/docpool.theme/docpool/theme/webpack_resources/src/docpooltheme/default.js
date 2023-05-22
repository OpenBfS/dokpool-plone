import "plone";

// Gets all needed less for plone and the theme
import "./default.less";
import "./theme.less";

import jQuery from "jquery";
import registry from "pat-registry";

/* facetednavigation */
if (
  jQuery(
    "body.template-facetednavigation_view,body.template-configure_faceted-html"
  ).length
) {
  (function () {
    "use strict";
    let faceted_evt = null,
      faceted_path = null;
    window.Faceted = {
      Load: function (evt, path) {
        faceted_evt = evt;
        faceted_path = path;
      },
    };
    Promise.all([
      import(/* webpackChunkName: "facetednavigation" */ "./facetednavigation"),
      import(/* webpackChunkName: "faceted-z3ctable" */ "./faceted-z3ctable"),
    ]).then((args) => {
      jQuery(document).ready(function (evt) {
        window.Faceted.Load(faceted_evt, faceted_path);
        // We use patterns inside the result of eea. So wait for it to be populated.
        if (typeof Faceted !== "undefined") {
          $(Faceted.Events).bind(
            Faceted.Events.AJAX_QUERY_SUCCESS,
            function () {
              // Async import the contentloader and do a mockup registry scan
              Promise.all([
                import(
                  /* webpackChunkName: "pat-contentloader-bfs" */ "./pattern/pat-contentloader-bfs"
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
            }
          );
        }
      });
    });
  })();
}
if (jQuery("body.template-configure_faceted-html").length) {
  (function () {
    "use strict";
    let faceted_evt = null,
      faceted_path = null;
    window.FacetedEdit = {
      Load: function (evt, path) {
        faceted_evt = evt;
        faceted_path = path;
      },
    };
    Promise.all([
      import(
        /* webpackChunkName: "facetednavigation-edit" */ "./facetednavigation-edit"
      ),
      import(
        /* webpackChunkName: "faceted-z3ctable" */ "./faceted-z3ctable-edit"
      ),
    ]).then((args) => {
      window.FacetedEdit.Load(faceted_evt, faceted_path);
    });
  })();
}

// More on magic comments
// https://webpack.js.org/api/module-methods/#magic-comments
// Imports the js for logged-in users
if (jQuery("body.userrole-anonymous").length === 0) {
  import(/* webpackChunkName: "logged-in" */ "./logged-in");
  import(/* webpackChunkName: "docpool-menu" */ "docpool-menu");
  import(/* webpackChunkName: "docpool" */ "./docpool");
}

// Imports the js/less for Openlayers
if (
  jQuery("body.portaltype-dpevent").length === 1 ||
  jQuery("body.template-dpevent").length === 1
) {
  import("./OpenLayer");
}

// Imports the js/less for popups
if (
  jQuery("#portal-column-content.bfs_popup").length === 1 ||
  jQuery("body.viewpermission-elan-journal-add-journalentry").length === 1
) {
  import("./popup.less");
}

// Imports the less for docpool-nonadmin bundle / simplify.less
// Replaces expression: python:not object.isAdmin() and not object.isContentAdmin()
if (jQuery("body.userrole-member").length === 1) {
  import("./nonadmin.less");
}

// Imports the less for removed docpool-anon bundle
// Replaces expression: python: member is None
if (jQuery("body.userrole-anonymous").length === 1) {
  import("./anonymous.less");
}

/* Expose jQuery when needed */
window.jQuery = jQuery;
window.$ = jQuery;
window.close_overview = close_popups;

import requirejs from "exports-loader?requirejs!script-loader!requirejs/require.js";
requirejs.config({}); // the real configuration is loaded in webpack.xml

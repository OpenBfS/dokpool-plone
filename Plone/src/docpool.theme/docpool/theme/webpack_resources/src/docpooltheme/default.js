import 'plone';

// Gets all needed less for plone and the theme
import './default.less';
import './theme.less';

import jQuery from 'jquery';
import registry from 'pat-registry';

// Todo Needs a place to stay (own file)
function makePopUp(thiswidth, thisheight, thisDocument, thisWindowName, thisXPosition, thisYPosition, thisScrollbar, thisResize) {
    'use strict';
    var myProperty = 'toolbar=0,location=0,directories=0,status=0,scrollbars=' + thisScrollbar + ',resizable=' + thisResize + ',width=' + thiswidth + ',height=' + thisheight + ',top=' + 0 + ',left=' + 0;
    var portal_root = $("body").data('portal-url');
    // Removes the host - shows only path
    var path_names = window.location.href.replace(portal_root,"");
    // Generates a unique window name like "Overview - Hessen" or "Overview - Bund"
    var generic_window_name = thisWindowName + "-" + path_names.split('/')[1];
    // Add to open_popups
    // XXX open_popups should really be a set of unique names
    let open_popups = JSON.parse(localStorage.getItem("open_popups"));
    if (open_popups === null) {
        open_popups = [];
    }
    open_popups.push(generic_window_name);
    localStorage.setItem("open_popups", JSON.stringify(open_popups));
    // Open popup if it doesn't yet exist, or reopen if it was closed
    if (!window['popup_' + generic_window_name] || window['popup_' + generic_window_name].closed === true) {
        window['popup_' + generic_window_name] = window.open(thisDocument, generic_window_name, myProperty);
    }
    window['popup_' + generic_window_name].focus();
}

// Todo Needs a place to stay (own file)
function go_to(url) {
    'use strict';
    // See https://redmine-koala.bfs.de/issues/4040#note-11
    var valid_urls = ['dokpool', 'Plone', 'dp_school'];
    var i = 0;
    var from_popup = false;
    // opener is the reference to
    // 1: the popup window opened it
    // 2: or the start page (www.imis.bfs.de/start)
    if (opener != null) {
        while (valid_urls[i]) {
            // Check if we are inside dokpool
            if (opener.document.location.href && opener.document.location.href.indexOf(valid_urls[i]) > -1) {
                from_popup = true;
                opener.focus();
                opener.document.location = url;
            }
            i++;
        }
        // Not opened from a popup so we open it in the main window
        if (!from_popup) {
            window.location.href = url;
        }
    } else {
        window.location.href = url;
    }
}

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
            }
        };
        Promise.all([
            import(
                /* webpackChunkName: "facetednavigation" */ "./facetednavigation"
                ),
            import(
                /* webpackChunkName: "faceted-z3ctable" */ "./faceted-z3ctable"
                )
        ]).then(args => {
            jQuery(document).ready(function (evt) {
                window.Faceted.Load(faceted_evt, faceted_path);
                // We use patterns inside the result of eea. So wait for it to be populated.
                if (typeof Faceted !== 'undefined') {
                    $(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function () {
                        // Async import the contentloader and do a mockup registry scan
                        Promise.all([
                            import(
                                /* webpackChunkName: "pat-contentloader-bfs" */ "./pattern/pat-contentloader-bfs"
                                )
                        ]).then(args => {
                            registry.scan($('#content-core'));
                        });
                        // Open all metatitle
                        $('#z3ctabel-toggles .z3ctable-toggle-metatitle').on('click', function (e) {
                            var open_state_title = false;
                            if ($(this).hasClass('state_open')){
                               open_state_title = true;
                                $(this).removeClass('state_open');
                            } else {
                                open_state_title = false;
                                $(this).addClass('state_open');
                            }
                            e.preventDefault();
                            $("#faceted_table .metatitle").each(function() {
                                // Its already open -> dont toggle
                                if (!$(this).hasClass('close')){
                                    $(this).click();
                                }
                            });
                            if (open_state_title){
                                $("#faceted_table .metatitle").click();
                            }
                        });
                        // Open all metainfos
                        $('#z3ctabel-toggles .z3ctable-toggle-metadata').on('click', function (e) {
                            var open_state_data = false;
                            if ($(this).hasClass('state_open')){
                                open_state_data = true;
                                $(this).removeClass('state_open');
                            } else {
                                open_state_data = false;
                                $(this).addClass('state_open');
                            }
                            e.preventDefault();
                            $("#faceted_table .metadata").each(function() {
                                // Its already open -> dont toggle
                                if (!$(this).hasClass('close')){
                                    $(this).click();
                                }
                            });
                            if (open_state_data){
                                $("#faceted_table .metadata").click();
                            }

                        });
                    });
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
            }
        };
        Promise.all([
            import(
                /* webpackChunkName: "facetednavigation-edit" */ "./facetednavigation-edit"
                ),
            import(
                /* webpackChunkName: "faceted-z3ctable" */ "./faceted-z3ctable-edit"
                ),
        ]).then(args => {
            window.FacetedEdit.Load(faceted_evt, faceted_path);
        });
    })();
}

// Todo Needs a place to stay (own file)
function close_popups() {
    let open_popups = JSON.parse(localStorage.getItem("open_popups"));
    if (open_popups !== null) {
        open_popups.forEach(function (item) {
            let popup = window.open('', item, '');
            if (popup) {
                popup.close();
            }
            delete window['popup_' + item];
        });
        localStorage.removeItem('open_popups');
    }
    var portal_root = $("body").data('portal-url');
    window.location.href = portal_root + '/logout';
}

// More on magic comments
// https://webpack.js.org/api/module-methods/#magic-comments
// Imports the js for logged-in users
if (jQuery('body.userrole-anonymous').length === 0) {
    import(/* webpackChunkName: "logged-in" */ './logged-in');
    import(/* webpackChunkName: "docpool-menu" */ 'docpool-menu');
    import(/* webpackChunkName: "jquery-marquee" */ 'jquery-marquee');
    import(/* webpackChunkName: "docpool" */ 'docpool');
}

// Imports the js/less for Openlayers
if ((jQuery('body.portaltype-dpevent').length === 1)
    || (jQuery('body.template-dpevent').length === 1)){
    import("./OpenLayer");
}

// Imports the js/less for popups
if ((jQuery('#portal-column-content.bfs_popup').length === 1)
    || (jQuery('body.viewpermission-elan-journal-add-journalentry').length === 1)){
    import("./Popup");
}

// Imports the less for docpool-nonadmin bundle / simplify.less
// Replaces expression: python:not object.isAdmin() and not object.isContentAdmin()
if (jQuery('body.userrole-member').length === 1) {
    import("./nonadmin.less");
}

// Imports the less for removed docpool-anon bundle
// Replaces expression: python: member is None
if (jQuery('body.userrole-anonymous').length === 1) {
    import("./anonymous.less");
}

/* Expose jQuery when needed */
window.jQuery = jQuery;
window.$ = jQuery;
window.makePopUp = makePopUp;
window.go_to = go_to;
window.close_overview = close_popups;

import requirejs from 'exports-loader?requirejs!script-loader!requirejs/require.js';
requirejs.config({});  // the real configuration is loaded in webpack.xml

import 'plone';

// Gets all needed less for plone and the theme
import './default.less';
import './theme.less';

import jQuery from 'jquery';
import registry from 'pat-registry';

// Todo Needs a place to stay
function makePopUp(thiswidth, thisheight, thisDocument, thisWindowName, thisXPosition, thisYPosition, thisScrollbar, thisResize) {
    'use strict';
    var myProperty = 'toolbar=0,location=0,directories=0,status=0,scrollbars=' + thisScrollbar + ',resizable=' + thisResize + ',width=' + thiswidth + ',height=' + thisheight + ',top=' + 0 + ',left=' + 0;
    var portal_root = $("body").data('portal-url');
    // Removes the host - shows only path
    var path_names = window.location.href.replace(portal_root,"");
    // Generates a unique window name like "Overview - Hessen" or "Overview - Bund"
    var generic_window_name = thisWindowName + "-" + path_names.split('/')[1];
    window['popup_' + generic_window_name] = null;
    // No popup exists
    if (window['open_' + generic_window_name] === false || window['open_' + generic_window_name] === undefined) {
        window['popup_' + generic_window_name] = window.open(thisDocument, generic_window_name, myProperty);
        window['open_' + generic_window_name] = true;
        window['popup_' + generic_window_name].focus();
    }
    // Popup was closed and will be reopened
    if (window['popup_' + generic_window_name] && window['popup_' + generic_window_name].closed === true) {
        window['popup_' + generic_window_name] = window.open(thisDocument, generic_window_name, myProperty);
        window['popup_' + generic_window_name].focus();
    }
    // Popup is open and will be focused
    if (window['popup_' + generic_window_name] && window['popup_' + generic_window_name].closed === false) {
        window['popup_' + generic_window_name].focus();
    }
    // Popup open and no reload happend
    if (window['open_' + generic_window_name]){
        window['popup_' + generic_window_name] = window.open(thisDocument, generic_window_name, myProperty);
        window['popup_' + generic_window_name].focus();
    }
}

// Todo Needs a place to stay
function go_to(url) {
    'use strict';
    var valid_urls = ['dokpool', 'Plone'];
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
if (jQuery('body.template-facetednavigation_view').length === 1) {
    import(/* webpackChunkName: "faceted-navigation-expand" */ 'faceted-navigation-expand');
    import(/* webpackChunkName: "faceted-navigation-independent" */ 'faceted-navigation-independent');
    import(/* webpackChunkName: "faceted-widgets-alphabets-view" */ 'faceted-widgets-alphabets-view');
    import(/* webpackChunkName: "faceted-widgets-autocomplete-view" */ 'faceted-widgets-autocomplete-view');
    import(/* webpackChunkName: "faceted-widgets-checkbox-view" */ 'faceted-widgets-checkbox-view');
    import(/* webpackChunkName: "faceted-widgets-criteria-view" */ 'faceted-widgets-criteria-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-date-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-daterange-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-debug-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-etag-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-multiselect-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-path-tree');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-path-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-portlet-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-radio-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-range-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-resultsfilter-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-resultsperpage-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-select-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-sorting-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-tagscloud-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-tal-view');
    import(/* webpackChunkName: "docpool-functions" */ 'faceted-widgets-text-view');
    import(/* webpackChunkName: "faceted-view" */ 'faceted-navigation-view').then(() => {
    jQuery(($) => setTimeout(() => {debugger;
        Faceted.Load(evt, '');
    }, 0));
  });
}

// More on magic comments
// https://webpack.js.org/api/module-methods/#magic-comments
// Imports the js for logged-in users
if (jQuery('body.userrole-anonymous').length === 0) {
    import(/* webpackChunkName: "logged-in" */ './logged-in');
    import(/* webpackChunkName: "docpool-functions" */ 'docpool-functions');
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

// Imports the less for docpool-nonadmin bundle
// Replaces expression: python:not object.isAdmin() and not object.isContentAdmin()
if (jQuery('body.userrole-member').length === 1) {
    import("./nonadmin.less")
}

// Imports the js and less for docpool-anon bundle
// Replaces expression: python: member is None
if (jQuery('body.userrole-anonymous').length === 1) {
    import(/* webpackChunkName: "anonymous" */ './anonymous');
}

/* Expose jQuery when needed */
window.jQuery = jQuery;
window.$ = jQuery;
window.makePopUp = makePopUp;
window.go_to = go_to;

import requirejs from 'exports-loader?requirejs!script-loader!requirejs/require.js';
requirejs.config({});  // the real configuration is loaded in webpack.xml

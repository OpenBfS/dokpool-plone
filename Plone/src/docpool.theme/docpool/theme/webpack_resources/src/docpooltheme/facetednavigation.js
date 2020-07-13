import "ajaxfileupload";
import "++view++collective.js.jqueryui.custom.min.js";

import "imports-loader?jQuery=jquery!bbq";
import "imports-loader?jQuery=jquery!jstree";
import "imports-loader?jQuery=jquery!select2uislider";
import "imports-loader?jQuery=jquery!tagcloud";

import "expose-loader?Faceted!exports-loader?Faceted!faceted-navigation-view";

import "imports-loader?jQuery=jquery!faceted-navigation-expand";
import "imports-loader?jQuery=jquery!faceted-navigation-independent";
import "imports-loader?jQuery=jquery!faceted-widgets-alphabets-view";
import "imports-loader?jQuery=jquery!faceted-widgets-autocomplete-view";
import "imports-loader?jQuery=jquery!faceted-widgets-checkbox-view";
import "imports-loader?jQuery=jquery!faceted-widgets-criteria-view";
import "imports-loader?jQuery=jquery!faceted-widgets-date-view";
import "imports-loader?jQuery=jquery!faceted-widgets-daterange-view";
import "imports-loader?jQuery=jquery!faceted-widgets-debug-view";
import "imports-loader?jQuery=jquery!faceted-widgets-etag-view";
import "imports-loader?jQuery=jquery!faceted-widgets-multiselect-view";
import "imports-loader?jQuery=jquery!faceted-widgets-path-tree";
import "imports-loader?jQuery=jquery!faceted-widgets-path-view";
import "imports-loader?jQuery=jquery!faceted-widgets-portlet-view";
import "imports-loader?jQuery=jquery!faceted-widgets-radio-view";
import "imports-loader?jQuery=jquery!faceted-widgets-range-view";
import "imports-loader?jQuery=jquery!faceted-widgets-resultsfilter-view";
import "imports-loader?jQuery=jquery!faceted-widgets-resultsperpage-view";
import "imports-loader?jQuery=jquery!faceted-widgets-select-view";
import "imports-loader?jQuery=jquery!faceted-widgets-sorting-view";
import "imports-loader?jQuery=jquery!faceted-widgets-tagscloud-view";
import "imports-loader?jQuery=jquery!faceted-widgets-tal-view";
import "imports-loader?jQuery=jquery!faceted-widgets-text-view";

import "./facetednavigation.less";
import jQuery from "jquery";

if (typeof window.Faceted !== "undefined") {
  Faceted.Options.FADE_SPEED = 0;
}

jQuery(function($) {
  "use strict";

  if ($.datepicker) {
    $.datepicker.setDefaults(
      $.datepicker.regional[$("html").attr("lang") || "de"]
    );
  }
});
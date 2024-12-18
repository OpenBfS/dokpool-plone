import { go_to } from "./window_functions";
import { close_popups } from "./window_functions";
import { makePopUp } from "./window_functions";
import jQuery from "jquery";
import $ from "jquery";
import { getURLParam } from "./utils";

// Global functions needed in window
window.go_to = go_to;
window.makePopUp = makePopUp;
window.close_overview = close_popups;
window.jQuery = jQuery;
window.$ = jQuery;

// Global styles
import("./docpool_styles/header-timetable.scss");
import("./docpool_styles/footer.scss");

// Test for the first css selectors, returns null if not found otherwise returns the element
const isAnonymous = document.querySelector(".userrole-anonymous");

// Logged-In users
if (isAnonymous == null) {
  import("./theme.scss");
}

// Anonymous users
if (isAnonymous != null) {
  import("./docpool_styles/anonymous.scss");
}

// Imports the scss for docpool-nonadmin bundle / simplify.less
// Replaces expression: not:object/@@is/admin_or_contentadmin
const isMember = document.querySelector(".userrole-member");
if (isMember !== null) {
  import("./docpool_styles/nonadmin.scss");
}

jQuery(document).on("click", ".collapsible", function () {
  this.classList.toggle("active");
  var content = this.nextElementSibling;
  if (content.style.maxHeight) {
    content.style.maxHeight = null;
  } else {
    content.style.maxHeight = content.scrollHeight + "px";
  }
});

// Resets filter in the Chronologie popup
const categoriesForm = document.getElementById("categories");
const categoriesSelect = document.getElementById("cat_select");

jQuery(document).on("click", ".cat_filter #reset_filter", function () {
  event.preventDefault();
  categoriesSelect.value = "";
  categoriesForm.submit();
});

$(function () {
  // Adds the docType string to the edit heading
  // https://redmine-koala.bfs.de/issues/5282
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
});

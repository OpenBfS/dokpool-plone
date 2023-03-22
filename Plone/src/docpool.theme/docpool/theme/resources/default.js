import { go_to } from "./window_functions";
import { makePopUp } from "./window_functions";
import $ from "jquery";

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

$(document).on("click", ".collapsible", function (event) {
  this.classList.toggle("active");
  var content = this.nextElementSibling;
  if (content.style.maxHeight) {
    content.style.maxHeight = null;
  } else {
    content.style.maxHeight = content.scrollHeight + "px";
  }
});

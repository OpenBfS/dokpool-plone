import "@patternslib/patternslib/src/globals";
import { go_to } from "./window_functions";
import { makePopUp } from "./window_functions";

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

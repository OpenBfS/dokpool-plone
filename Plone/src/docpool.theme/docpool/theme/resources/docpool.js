import { go_to } from "./window_functions";
import { makePopUp } from "./window_functions";

// Global functions needed in window
window.go_to = go_to;
window.makePopUp = makePopUp;

// Logged-In users
if (document.querySelector(".userrole-anonymous") === null) {
  import("./theme.scss");
}

// Anonymous users
if (document.querySelector(".userrole-anonymous") !== null) {
  import("./docpool_styles/anonymous.scss");
}

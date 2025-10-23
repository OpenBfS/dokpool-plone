export function go_to(url) {
  "use strict";
  // See https://redmine-koala.bfs.de/issues/4040#note-11
  var valid_urls = ["dokpool", "Plone", "dp_school"];
  var i = 0;
  var from_popup = false;
  // opener is the reference to
  // 1: the popup window opened it
  // 2: or the start page (www.imis.bfs.de/start)
  if (opener != null) {
    while (valid_urls[i]) {
      // Check if we are inside dokpool
      if (
        opener.document.location.href &&
        opener.document.location.href.indexOf(valid_urls[i]) > -1
      ) {
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

export function makePopUp(
  thiswidth,
  thisheight,
  thisDocument,
  thisWindowName,
  thisXPosition,
  thisYPosition,
  thisScrollbar,
  thisResize,
) {
  "use strict";
  var myProperty =
    "toolbar=0,location=0,directories=0,status=0,scrollbars=" +
    thisScrollbar +
    ",resizable=" +
    thisResize +
    ",width=" +
    thiswidth +
    ",height=" +
    thisheight +
    ",top=" +
    0 +
    ",left=" +
    0;
  var portal_root = $("body").data("portal-url");
  // Removes the host - shows only path
  var path_names = window.location.href.replace(portal_root, "");
  // Generates a unique window name like "Overview - Hessen" or "Overview - Bund"
  var generic_window_name = thisWindowName + "-" + path_names.split("/")[1];
  // Add to open_popups
  // XXX open_popups should really be a set of unique names
  let open_popups = JSON.parse(localStorage.getItem("open_popups"));
  if (open_popups === null) {
    open_popups = [];
  }
  open_popups.push(generic_window_name);
  localStorage.setItem("open_popups", JSON.stringify(open_popups));
  // Open popup if it doesn't yet exist, or reopen if it was closed
  if (
    !window["popup_" + generic_window_name] ||
    window["popup_" + generic_window_name].closed === true
  ) {
    window["popup_" + generic_window_name] = window.open(
      thisDocument,
      generic_window_name,
      myProperty,
    );
  }
  window["popup_" + generic_window_name].focus();
}
export function close_popups() {
  let open_popups = JSON.parse(localStorage.getItem("open_popups"));
  if (open_popups !== null) {
    open_popups.forEach(function (item) {
      let popup = window.open("", item, "");
      if (popup) {
        popup.close();
      }
      delete window["popup_" + item];
    });
    localStorage.removeItem("open_popups");
  }
  var portal_root = $("body").data("portal-url");
  window.location.href = portal_root + "/logout";
}

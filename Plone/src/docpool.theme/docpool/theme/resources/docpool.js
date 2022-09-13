function go_to(url) {
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

window.go_to = go_to;

// On the same site it saves the popup
var windowObjectReference = null;

var thisY=0;
var thisX=0;

function makePopUp(thiswidth, thisheight, thisDocument, thisWindowName, thisXPosition, thisYPosition, thisScrollbar, thisResize) {
	'use strict';
	var myProperty = 'toolbar=0,location=0,directories=0,status=0,scrollbars=' + thisScrollbar + ',resizable=' + thisResize + ',width=' + thiswidth + ',height=' + thisheight + ',top=' + thisY + ',left=' + thisX;
	// Generates a unique window name like "Overview - Hessen" or "Overview - Bund"
	var path_names = window.location.pathname.split('/');
	var generic_window_name = thisWindowName + "-" + path_names[path_names.length - 2];
	// Test if the popup is closed, if not open
    if(windowObjectReference == null || windowObjectReference.closed) {
        windowObjectReference = window.open(thisDocument, generic_window_name, myProperty);
    } else {
        windowObjectReference.focus();
    }
}

function go_to(url) {
	'use strict';
	if (opener != null) {
		opener.focus(); 	 
		opener.document.location = url;
	} else {
		window.location.href = url;
	}
  }

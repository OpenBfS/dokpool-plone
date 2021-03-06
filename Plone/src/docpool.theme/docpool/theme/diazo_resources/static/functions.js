var thisY=0;
var thisX=0;
function makePopUp(thiswidth, thisheight, thisDocument, thisWindowName, thisXPosition, thisYPosition, thisScrollbar, thisResize) {
    'use strict';
    var myProperty = 'toolbar=0,location=0,directories=0,status=0,scrollbars=' + thisScrollbar + ',resizable=' + thisResize + ',width=' + thiswidth + ',height=' + thisheight + ',top=' + thisY + ',left=' + thisX;
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
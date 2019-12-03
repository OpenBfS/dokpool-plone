var thisY=0;
var thisX=0;

function getPopup(name) {
    'use strict';
    //Get the window
    let chron_bund=window.open('',name,'');
    // The closed property is true if the window is closed.
    if (!chron_bund.closed){
        return chron_bund
    }
}

function makePopUp(thiswidth, thisheight, thisDocument, thisWindowName, thisXPosition, thisYPosition, thisScrollbar, thisResize) {
    'use strict';
    let myProperty = 'toolbar=0,location=0,directories=0,status=0,scrollbars=' + thisScrollbar + ',resizable=' + thisResize + ',width=' + thiswidth + ',height=' + thisheight + ',top=' + thisY + ',left=' + thisX;
    // Generates a unique window name like "Overview - Hessen" or "Overview - Bund"
    let path_names = window.location.pathname.split('/');
    let generic_window_name = thisWindowName + "-" + path_names[path_names.length - 2];
    let open_popup= getPopup(generic_window_name);
    if (typeof (open_popup) == 'undefined'){
        // Popup does not exists, we open it
        console.log('Open Popup: ' + generic_window_name);
        window.open(thisDocument, generic_window_name, myProperty);

    } else {
        console.log('Focus Popup:' + generic_window_name);
        open_popup.focus();
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

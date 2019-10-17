var LastWindowOpened = "";

var thisY=0;
var thisX=0;

function makePopUp(thiswidth,thisheight,thisDocument,thisWindowName,thisXPosition,thisYPosition,thisScrollbar,thisResize) {
	myProperty = 'toolbar=0,location=0,directories=0,status=0,scrollbars=' + thisScrollbar + ',resizable=' + thisResize + ',width=' + thiswidth + ',height=' + thisheight + ',top=' + thisY + ',left=' + thisX;
	// Generates a unique window name like "Overview - Hessen" or "Overview - Bund"
	path_names = window.location.pathname.split('/');
	generic_window_name = thisWindowName + "-" + path_names[path_names.length -2];
    window.open(thisDocument,generic_window_name,myProperty);
}


function go_to(url) {
	if (opener != null) {
		opener.focus(); 	 
		opener.document.location = url;
	} else {
		window.location.href = url;
	}
  }

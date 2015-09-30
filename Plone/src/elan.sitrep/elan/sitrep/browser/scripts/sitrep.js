
function insertTextblock () {
	 window.opener.$("#foo").html("bar");
	   var intercom = Intercom.getInstance();
	    intercom.emit('notice', {message: 'Hello, all windows!'});	 
}

$(document).ready ( function () {

} );

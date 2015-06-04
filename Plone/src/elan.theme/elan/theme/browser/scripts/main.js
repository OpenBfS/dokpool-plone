var LastWindowOpened = "";
	
var thisY=0;
var thisX=0;

function makePopUp(thiswidth,thisheight,thisDocument,thisWindowName,thisXPosition,thisYPosition,thisScrollbar,thisResize) {
	myProperty = 'toolbar=0,location=0,directories=0,status=0,scrollbars=' + thisScrollbar + ',resizable=' + thisResize + ',width=' + thiswidth + ',height=' + thisheight + ',top=' + thisY + ',left=' + thisX;
	
	if(self.myWindow == null){
		delete myWindow;
		myWindow = window.open(thisDocument,thisWindowName,myProperty);
		if(myWindow != null){
			myWindow.focus();
		}
	}
	else{
		if(!(myWindow.closed)){
			self.myWindow.close();
			myWindow  = window.open(thisDocument,thisWindowName,myProperty);
		}
		else{
			myWindow  = window.open(thisDocument,thisWindowName,myProperty);
		}
	}
}


function go_to(url) {
	if (opener != null) {
		opener.focus(); 	 
		opener.document.location = url;
	} else {
		window.location.href = url;
	}
  }

function loadDyn () {
	jQuery("#mesz").load ("refresh_time #time_table");
	jQuery("dl.portletRecent").load ("refresh_recent #recent_content");
}

jQuery(document).ready ( function () {
	myDynTimer = setInterval ( loadDyn, 60000 );
	jQuery('.documentByLine a').removeAttr('href').addClass('commentator');
	var type = jQuery('#form-widgets-docType')
	if (type[0] != null) {
		var option = type[0].options[type[0].selectedIndex];
		var value = option.text;
		var title = jQuery('h1.documentFirstHeading').text();
		jQuery('h1.documentFirstHeading').text(title + ' (' + value + ')'); 
	}
} );


jQuery(document).ready(function() {
	jQuery('table.elanlisting a.transfer').prepOverlay({
	    subtype: 'ajax',
	    //filter: '#content>*',
	    formselector: 'form[name="transferform"]',
	    closeselector: '[name="form.button.cancel"]',
	    noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'redirect');},
    	//redirect: jq.plonepopups.redirectbasehref
	    //noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'reload');}
	    //noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'close');}
	    /*noform: 'redirect',*/
	    redirect: jQuery('#redirecturl').text()
	    
	});
});
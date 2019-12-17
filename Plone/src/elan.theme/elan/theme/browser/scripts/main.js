var LastWindowOpened = "";
	
var thisY=0;
var thisX=0;

function go_to(url) {
	'use strict';
	var valid_urls = ['dokpool', 'Plone'];
	var i = 0;
	// opener is the reference to the window opened here
	if (opener != null) {
		// Check if we are inside dokpool
		while (valid_urls[i]) {
			if (opener.document.location.href && opener.document.location.href.indexOf(valid_urls[i]) > -1) {
				opener.focus();
				opener.document.location = url;
			}
			i++;
		}
	} else {
		window.location.href = url;
	}
}

function loadDyn () {
	$("#mesz").load ("refresh_time #time_table");
	$("dl.portletRecent").load ("refresh_recent #recent_content");
}

$(document).ready ( function () {
	myDynTimer = setInterval ( loadDyn, 60000 );
	$('.documentByLine a').removeAttr('href').addClass('commentator');
	var type = $('#form-widgets-docType')
	if (type[0] != null) {
		var option = type[0].options[type[0].selectedIndex];
		var value = option.text;
		var title = $('h1.documentFirstHeading').text();
		$('h1.documentFirstHeading').text(title + ' (' + value + ')'); 
	}
} );


$(document).ready(function() {
	$('table.elanlisting a.transfer').prepOverlay({
	    subtype: 'ajax',
	    //filter: '#content>*',
	    formselector: 'form[name="transferform"]',
	    closeselector: '[name="form.button.cancel"]',
	    noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'redirect');},
    	//redirect: jq.plonepopups.redirectbasehref
	    //noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'reload');}
	    //noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'close');}
	    /*noform: 'redirect',*/
	    redirect: $('#redirecturl').text()
	    
	});
});
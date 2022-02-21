var LastWindowOpened = "";
	
var thisY=0;
var thisX=0;

function go_to(url) {
	'use strict';
	// See https://redmine-koala.bfs.de/issues/4040#note-11
	var valid_urls = ['dokpool', 'Plone', 'dp_school'];
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

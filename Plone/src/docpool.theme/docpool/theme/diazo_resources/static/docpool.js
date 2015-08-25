require(['jquery',
         'jquery-marquee',
         ], function($) {
	'use strict';
	
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
		$("#mesz").load ("refresh_time #time_table");
		$("section.portletRecent").load ("refresh_recent #recent_content");
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
		$('.marquee').marquee({
			pauseOnHover:true,
			duration: 10000,
		    //gap in pixels between the tickers
		    gap: 50,		
		    }
				
		);
	} );


/*	$(document).ready(function() {
		$('table.elanlisting a.transfer').prepOverlay({
		    subtype: 'ajax',
		    //filter: '#content>*',
		    formselector: 'form[name="transferform"]',
		    closeselector: '[name="form.button.cancel"]',
		    noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'redirect');},
	    	//redirect: jq.plonepopups.redirectbasehref
		    //noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'reload');}
		    //noform: function(el) {return jq.plonepopups.noformerrorshow(el, 'close');}
		    noform: 'redirect',
		    redirect: $('#redirecturl').text()
		    
		});
	});	
*/
	});

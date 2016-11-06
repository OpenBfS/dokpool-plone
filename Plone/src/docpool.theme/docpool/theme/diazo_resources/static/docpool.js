require(['jquery',
         'intercom',
         'notify',
         'docpool-functions',
         'jquery-marquee',
         'domReady!'
         ], function($) {
	'use strict';

	function loadDyn () {
		$("#mesz").load ("refresh_time #time_table");
		$("section.portletRecent").load ("refresh_recent #recent_content");
	}

	myDynTimer = setInterval ( loadDyn, 60000 );
	$('.documentByLine a').removeAttr('href').addClass('commentator');
	var type = $('#form-widgets-docType')
	if ((type[0] != null) && (type[0].selectedIndex != null)) {
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
});

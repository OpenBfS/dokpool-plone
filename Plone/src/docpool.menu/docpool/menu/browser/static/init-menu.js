require(['jquery',
         'docpool-menu'
         ], function($, Registry) {
	'use strict';

	$().ready(function() {
		var menu = $('.rm-nav').rMenu({
			minWidth: '960px',
			toggleBtnBool: false,
		});
	});

});
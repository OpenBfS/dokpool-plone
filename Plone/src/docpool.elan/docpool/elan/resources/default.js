// docpool.elan js/scss entry

import $ from "jquery";
import "jquery.marquee";
import("./styles.scss");

$(function () {
  $(".marquee").marquee({
    pauseOnHover: true,
    duration: 10000,
    //gap in pixels between the tickers
    gap: 50,
  });
});

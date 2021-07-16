export function sortUnorderedList(ul, sortDescending) {
  'use strict';

  if(typeof ul === "string") {
    ul = document.querySelectorAll(ul)[0];
  }

  // Get the list items and setup an array for sorting
  var lis = ul.getElementsByTagName("LI");
  var vals = [];

  // Populate the array
  for(var i = 0, l = lis.length; i < l; i++) {
    vals.push(lis[i].innerHTML);
  }

  // Sort it
  vals.sort();

  // Sometimes you gotta DESC
  if(sortDescending) {
    vals.reverse();

  }

  // Change the list on the page
  for(var i = 0, l = lis.length; i < l; i++) {
    lis[i].innerHTML = vals[i];
  }
}

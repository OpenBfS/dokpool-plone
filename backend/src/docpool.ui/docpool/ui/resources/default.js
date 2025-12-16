import "bootstrap";
import "./docpool.scss";
// Pat-update-notification
import("./pat-update-notification/index.js");
import registry from "@patternslib/patternslib/src/core/registry";

document.addEventListener("patterns-injected-delayed", (e) => {
  if (!(e.target instanceof Element)) return;

  if (!e.target.matches("#content.container")) return;

  const $navContainer = $(".list-group[data-current-item]");

  // Add saved query string to back link (listing), if present
  const savedQuery = localStorage.getItem("dokpool-listing-query");
  if (savedQuery && savedQuery.length > 0) {
    const $backLink = $navContainer.find(".list-group-item.back a");
    const backHref = $backLink.attr("href");
    if (backHref && !backHref.includes("?")) {
      $backLink.attr("href", `${backHref}?${savedQuery}`);
    }
  }

  // TODO Cleanup duplicate code
  const currentUid = $navContainer.data("current-item");
  var $nextLink = $navContainer.find(".list-group-item.next a");
  if ($nextLink.length > 0) {
    var newNextUrl = getNeighborUrl(currentUid, "next");
    $nextLink.attr("href", newNextUrl);
    console.log("Inject fertig (next-item):", newNextUrl);
  }
  registry.scan($nextLink[0]);

  var $prevLink = $navContainer.find(".list-group-item.prev a");
  if ($prevLink.length > 0) {
    var newPrevUrl = getNeighborUrl(currentUid, "prev");
    console.log("Inject fertig (prev-item):", newPrevUrl);
    $prevLink.attr("href", newPrevUrl);
  }
  registry.scan($prevLink[0]);
});

function getNeighborUrl(currentUid, direction) {
  const savedListStr = localStorage.getItem("dokpool-listing-items");
  if (!savedListStr) return null;

  const list = JSON.parse(savedListStr);
  const index = list.indexOf(currentUid);

  if (index === -1) return null;

  let targetUid = null;

  // TODO Check there is really a next / prev item
  if (direction === "prev") {
    targetUid = list[index - 1];
  } else if (direction === "next") {
    targetUid = list[index + 1];
  }
  let baseUrl = document.body.dataset.portalUrl;

  // TODO Find url of current dokpool
  return targetUid ? baseUrl + `/resolveuid/${targetUid}` : null;
}

$(document).on("click", "a.pat-inject.list-item-link", function (e) {
  // TODO Find correct event / click - if there is a better on??

  const listing = $("#listing");
  if (listing.length > 0) {
    // Save the (filtered) list into localstorage
    const items = listing.data("items");
    if (items) {
      localStorage.setItem("dokpool-listing-items", JSON.stringify(items));
      console.log("Localstorage saved", items.length);
    }
    // Save the filter query into localstorage
    const params = new URLSearchParams(window.location.search);
    // Override if empty
    localStorage.setItem("dokpool-listing-query", params.toString());
  }
});

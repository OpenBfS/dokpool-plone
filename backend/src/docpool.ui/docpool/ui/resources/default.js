import "bootstrap";
import "./docpool.scss";
// Pat-update-notification
import("./pat-update-notification/index.js");

function getNeighborUrl(currentUid, direction) {
  const savedListStr = localStorage.getItem("dokpool-listing-items");
  if (!savedListStr) return null;

  const list = JSON.parse(savedListStr);
  const index = list.indexOf(currentUid);

  if (index === -1) return null;

  let targetUid = null;

  if (direction === "prev" && index > 0) {
    targetUid = list[index - 1];
  } else if (direction === "next" && index < list.length - 1) {
    targetUid = list[index + 1];
  }
  let baseUrl = document.body.dataset.portalUrl;

  // TODO Find url of current dokpool
  return targetUid ? baseUrl + `/@@listing-item?uid=${targetUid}` : null;
}

$(document).on("click", "li.priv", function (e) {
  const $navContainer = $(".list-group[data-current-item]");
  const currentUid = $navContainer.data("current-item");
  var $privLink = $navContainer.find(".list-group-item.priv a");

  if ($privLink.length > 0) {
    var newPrivUrl = getNeighborUrl(currentUid, "prev");
    $privLink.attr("href", newPrivUrl);
  }
  $privLink.click();
});
$(document).on("click", "li.next", function (e) {
  const $navContainer = $(".list-group[data-current-item]");
  const currentUid = $navContainer.data("current-item");
  var $nextLink = $navContainer.find(".list-group-item.next a");
  if ($nextLink.length > 0) {
    var newNextUrl = getNeighborUrl(currentUid, "next");
    $nextLink.attr("href", newNextUrl);
  }
  $nextLink.click();
});

$(document).on("click", "a.pat-inject.list-item-link", function (e) {
  // TODO Find correct event / click ...

  console.log("Inject war erfolgreich", e);
  const $listing = $("#listing");
  if ($listing.length > 0) {
    const items = $listing.data("items");
    if (items) {
      localStorage.setItem("dokpool-listing-items", JSON.stringify(items));
      console.log("Localstorage saved");
    }
  }
});

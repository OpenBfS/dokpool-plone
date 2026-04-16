import "bootstrap";
// Pat-update-notification
import("./pat-update-notification/index.js");
import registry from "@patternslib/patternslib/src/core/registry";

const MOBILE_SCROLL_TOP_BREAKPOINT = 991;
const MOBILE_SCROLL_TOP_OFFSET = 240;

function setupMobileScrollTopButton() {
  const button = document.querySelector(".mobile-scroll-top-button");
  if (!button) return;

  const updateVisibility = () => {
    const isMobile = window.innerWidth <= MOBILE_SCROLL_TOP_BREAKPOINT;
    const shouldShow = isMobile && window.scrollY > MOBILE_SCROLL_TOP_OFFSET;
    button.hidden = !shouldShow;
    button.classList.toggle("is-visible", shouldShow);
  };

  button.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  window.addEventListener("scroll", updateVisibility, { passive: true });
  window.addEventListener("resize", updateVisibility);
  document.addEventListener("patterns-injected-delayed", updateVisibility);
  updateVisibility();
}

function setupMobileOffcanvasSettingsNavigation() {
  const offcanvasNavbar = document.getElementById("offcanvasNavbar");
  const mainTabTrigger = document.getElementById(
    "mobile-settings-main-tab-trigger",
  );
  if (!offcanvasNavbar || !mainTabTrigger) return;

  if (offcanvasNavbar.dataset.mobileSettingsResetBound === "1") {
    return;
  }
  offcanvasNavbar.dataset.mobileSettingsResetBound = "1";

  offcanvasNavbar.addEventListener("hidden.bs.offcanvas", () => {
    mainTabTrigger.click();
  });

  offcanvasNavbar
    .querySelectorAll("[data-mobile-settings-back='true']")
    .forEach((button) => {
      button.addEventListener("click", () => {
        mainTabTrigger.click();
      });
    });
}

function setupListingMobileFilters() {
  const dropdown = document.getElementById("listingMobileFiltersDropdown");
  if (!dropdown) return;
  const mainTabTrigger = document.getElementById(
    "mobile-listing-main-tab-trigger",
  );

  if (dropdown.dataset.mobileListingFiltersBound === "1") {
    return;
  }
  dropdown.dataset.mobileListingFiltersBound = "1";
  const backButtons = dropdown.querySelectorAll(
    "[data-mobile-listing-back='true']",
  );

  const resetToMainPane = () => {
    if (mainTabTrigger) {
      mainTabTrigger.click();
    }
  };

  backButtons.forEach((button) => {
    button.addEventListener("click", () => {
      resetToMainPane();
    });
  });

  dropdown.addEventListener("hidden.bs.dropdown", () => {
    resetToMainPane();
  });
}

function setupHeaderMobileUi() {
  setupMobileScrollTopButton();
  setupMobileOffcanvasSettingsNavigation();
  setupListingMobileFilters();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupHeaderMobileUi);
} else {
  setupHeaderMobileUi();
}

// After inject this code sets the back link to listing and populates next/prev links
document.addEventListener("patterns-injected-delayed", (e) => {
  if (!(e.target instanceof Element)) return;

  if (!e.target.matches("#content")) return;

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

  const currentUid = $navContainer.data("current-item");
  ["next", "prev"].forEach((dir) => {
    const $link = $navContainer.find(`.list-group-item.${dir} a`);
    if ($link.length > 0) {
      const newUrl = getNeighborUrl(currentUid, dir);
      if (newUrl) {
        $link.attr("href", newUrl);
      }
    }
    if ($link[0]) {
      registry.scan($link[0]);
    }
  });
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

// Saves ordered items from listing into localstorage
$(document).on("click", "a.pat-inject.list-item-link", function (e) {
  // TODO Find correct event / click - if there is a better one ??
  const listing = $("#listing");
  if (listing.length > 0) {
    // Save the (filtered) list into localstorage
    const items = listing.data("items");
    if (items) {
      localStorage.setItem("dokpool-listing-items", JSON.stringify(items));
    }
    // Save the filter query into localstorage
    const params = new URLSearchParams(window.location.search);
    // Override if empty
    localStorage.setItem("dokpool-listing-query", params.toString());
  }
});

import "bootstrap";
import "./upload";
import "@patternslib/patternslib/src/pat/expandable-tree/expandable-tree.css";
// Pat-update-notification
import("./pat-update-notification/index.js");
import registry from "@patternslib/patternslib/src/core/registry";

const MOBILE_SCROLL_TOP_BREAKPOINT = 991;
const MOBILE_SCROLL_TOP_OFFSET = 240;
const RECENT_SEARCHES_LIMIT = 10;

// Initializes the mobile scroll-to-top button behavior.
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

// Initializes off-canvas settings navigation on mobile devices.
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

// Initializes mobile filter controls on listing pages.
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

// Initializes desktop listing filter reset interactions.
function setupListingDesktopFilterResets() {
  const listingFilters = document.getElementById("listing-filters");
  if (!listingFilters) return;

  if (listingFilters.dataset.desktopFilterResetBound === "1") {
    return;
  }
  listingFilters.dataset.desktopFilterResetBound = "1";

  const resetIcons = listingFilters.querySelectorAll("[data-filter-reset-url]");

  resetIcons.forEach((resetIcon) => {
    const navigateToResetUrl = () => {
      const resetUrl = resetIcon.getAttribute("data-filter-reset-url");
      if (resetUrl) {
        window.location.href = resetUrl;
      }
    };

    resetIcon.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      navigateToResetUrl();
    });

    resetIcon.addEventListener("keydown", (event) => {
      if (!["Enter", " ", "Spacebar"].includes(event.key)) return;
      event.preventDefault();
      event.stopPropagation();
      navigateToResetUrl();
    });
  });
}

function setupHeaderMobileUi() {
  setupMobileScrollTopButton();
  setupMobileOffcanvasSettingsNavigation();
  setupListingMobileFilters();
  setupListingDesktopFilterResets();
  setupSearchContextDropdown();
  setupRecentSearches();
}

function setupSearchContextDropdown() {
  const searchbox = document.getElementById("portal-searchbox");
  if (!searchbox) return;

  if (searchbox.dataset.searchContextDropdownBound === "1") return;
  searchbox.dataset.searchContextDropdownBound = "1";

  const input = searchbox.querySelector("#search-context-scope-input");
  const label = searchbox.querySelector(".dp-search-context-current-label");
  const options = searchbox.querySelectorAll("[data-search-scope]");

  if (!(input instanceof HTMLInputElement) || !label || options.length === 0) {
    return;
  }

  options.forEach((option) => {
    option.addEventListener("click", () => {
      const scope = option.getAttribute("data-search-scope");
      const scopeLabel = option.getAttribute("data-search-scope-label");
      if (!scope || !scopeLabel) return;

      input.value = scope;
      label.textContent = scopeLabel;

      options.forEach((item) => {
        item.classList.toggle("selected", item === option);
      });
    });
  });
}

function setupRecentSearches() {
  const searchbox = document.getElementById("portal-searchbox");
  const form = document.getElementById("searchGadget_form");
  const input = document.getElementById("searchGadget");
  const container = document.getElementById("dp-recent-searches");
  const resetButton = document.getElementById("dp-recent-searches-reset");
  if (!searchbox || !form || !input || !container || !resetButton) return;
  const recentSearchesSection = container.closest(".dp-search-col-recent");

  if (form.dataset.recentSearchesBound === "1") return;
  form.dataset.recentSearchesBound = "1";

  const appScope = searchbox.dataset.appScope || "default";
  const storageKey = `dokpool-recent-searches::${appScope}`;

  const loadRecentSearches = () => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return [];
      return parsed
        .map((value) => (typeof value === "string" ? value.trim() : ""))
        .filter((value) => value.length > 0)
        .slice(0, RECENT_SEARCHES_LIMIT);
    } catch (error) {
      return [];
    }
  };

  const saveRecentSearches = (items) => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(items));
    } catch (error) {
      // no localStorage m
    }
  };

  const renderRecentSearches = (items) => {
    const hasItems = items.length > 0;

    container.replaceChildren();
    if (recentSearchesSection) {
      recentSearchesSection.classList.toggle("d-none", !hasItems);
    }
    resetButton.classList.toggle("d-none", !hasItems);
    items.forEach((term) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className =
        "dp-search-chip-outline d-inline-flex align-items-center rounded-pill bg-white";
      button.textContent = term;
      button.setAttribute("data-search-term", term);
      container.appendChild(button);
    });
  };

  const addRecentSearch = (term) => {
    const cleanTerm = term.trim();
    if (!cleanTerm) return;
    const items = loadRecentSearches().filter((item) => item !== cleanTerm);
    items.unshift(cleanTerm);
    const nextItems = items.slice(0, RECENT_SEARCHES_LIMIT);
    saveRecentSearches(nextItems);
    renderRecentSearches(nextItems);
  };

  renderRecentSearches(loadRecentSearches());

  form.addEventListener("submit", () => {
    addRecentSearch(input.value || "");
  });

  container.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    const button = target.closest("button[data-search-term]");
    if (!(button instanceof HTMLButtonElement)) return;

    const term = button.dataset.searchTerm || "";
    input.value = term;
    form.requestSubmit();
  });

  resetButton.addEventListener("click", () => {
    saveRecentSearches([]);
    renderRecentSearches([]);
  });
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
    if (
      backHref &&
      !$backLink.attr("data-came_from") &&
      !backHref.includes("?")
    ) {
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
  if (!targetUid) return null;
  const url = new URL(baseUrl + `/resolveuid/${targetUid}`);
  const came_from = document
    .querySelector(".list-group-item.back a")
    ?.getAttribute("data-came_from");
  if (came_from) url.searchParams.set("came_from", came_from);
  return url.href;
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

// Event from pat-upload
$(document).on("uploadAllCompleted", "#dpdocument-edit-upload", function () {
  document.getElementById("edit-attachments-refresh")?.click();
});

$(document).on(
  "click",
  ".attachment-move-up, .attachment-move-down",
  async function () {
    const button = this;
    const attachmentList = button.closest("#attachments");
    const subsetIds = Array.from(
      attachmentList.querySelectorAll("tr[data-attachment-id]"),
      (row) => row.dataset.attachmentId,
    );
    const params = new URLSearchParams({
      id: button.dataset.attachmentId,
      delta: button.classList.contains("attachment-move-up") ? "-1" : "1",
      subsetIds: JSON.stringify(subsetIds),
      _authenticator: button.dataset.authenticator,
    });

    button.disabled = true;
    try {
      const response = await fetch(button.dataset.moveUrl, {
        method: "POST",
        credentials: "same-origin",
        body: params,
      });
      const result = await response.json().catch(() => null);
      if (!response.ok || result?.status !== "success") {
        throw new Error(result?.msg || "Could not move attachment.");
      }
      attachmentList.querySelector("#attachments-order-refresh").click();
    } catch (error) {
      window.alert(error.message);
    } finally {
      button.disabled = false;
    }
  },
);

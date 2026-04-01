from playwright.sync_api import expect
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

import pytest


class TestMobileUI:
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=SITE_OWNER_NAME, roles=["Manager"])
        self.page = playwright_page_factory(username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD)
        self.plone_url = self.portal.absolute_url()

    def test_mobile_menu_open_close(self):
        """Test that mobile menu can be opened and closed in mobile viewport"""
        page = self.page
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        # Check that offcanvas menu exists but is not visible initially
        offcanvas = page.locator("#offcanvasNavbar")
        expect(offcanvas).to_be_attached()
        menu_toggle = page.locator("button.navbar-toggler.ms-2")
        expect(menu_toggle).to_be_visible()
        menu_toggle.click()
        expect(offcanvas).to_be_visible()

        # Verify initial event and switch to the normal case event.
        selected_event_title = page.locator(
            "#mobile-settings-pane-main .mobile-event-selected-content .fw-bold",
        ).first
        expect(selected_event_title).to_have_text("Normalfall")

        active_events_link = page.locator("#mobile-settings-tab-active-events")
        expect(active_events_link).to_be_visible()
        active_events_link.click()
        notfall_link = page.get_by_role("link", name="Notfall")
        expect(notfall_link).to_be_visible()
        notfall_link.click()
        page.wait_for_load_state("networkidle")

        menu_toggle = page.locator("button.navbar-toggler.ms-2")
        expect(menu_toggle).to_be_visible()
        menu_toggle.click()

        selected_event_title = page.locator(
            "#mobile-settings-pane-main .mobile-event-selected-content .fw-bold",
        ).first
        expect(selected_event_title).to_have_text("Notfall")

        close_button = page.locator("#offcanvasNavbar button.mobile-offcanvas-close")
        expect(close_button).to_be_visible()
        close_button.click()
        expect(offcanvas).not_to_be_visible()

    def test_mobile_search_open_close(self):
        """Test that search can be opened and closed in mobile viewport"""
        page = self.page
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{self.plone_url}/bund")
        search_button = page.locator(".mobile-search-btn")
        expect(search_button).to_be_visible()
        search_button.click()
        # Check that search input is visible
        search_input = page.locator("input[type='search'], input[name='SearchableText']")
        expect(search_input.first).to_be_visible()
        page.locator(".dp-search-dismiss").click()
        # Searchbox should be hidden or collapsed
        expect(search_input).not_to_be_visible()

    def test_mobile_scroll_top_button(self):
        """Test that mobile scroll-to-top button is shown only when needed and works."""
        page = self.page
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{self.plone_url}/bund")

        button = page.locator(".mobile-scroll-top-button")
        expect(button).to_be_hidden()

        # Ensure the page can scroll on small test fixtures.
        page.evaluate("document.body.style.minHeight = '3000px'")
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_function("window.scrollY > 240")
        expect(button).to_be_visible()

        button.click()
        page.wait_for_function("window.scrollY <= 5")
        expect(button).to_be_hidden()

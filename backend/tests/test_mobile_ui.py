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
        page.goto(f"{self.plone_url}")
        # Check that offcanvas menu exists but is not visible initially
        offcanvas = page.locator("#offcanvasNavbar")
        expect(offcanvas).to_be_attached()
        menu_toggle = page.locator("button.navbar-toggler.ms-2")
        expect(menu_toggle).to_be_visible()
        menu_toggle.click()
        expect(offcanvas).to_be_visible()
        close_button = page.locator("#offcanvasNavbar button.btn-close")
        expect(close_button).to_be_visible()
        close_button.click()

    def test_mobile_search_open_close(self):
        """Test that search can be opened and closed in mobile viewport"""
        page = self.page
        # Set mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{self.plone_url}")
        search_button = page.locator(".mobile-search-btn")
        expect(search_button).to_be_visible()
        search_button.click()
        # Check that search input is visible
        search_input = page.locator("input[type='search'], input[name='SearchableText']")
        expect(search_input.first).to_be_visible()
        page.locator(".dp-search-dismiss").click()
        # Searchbox should be hidden or collapsed
        expect(search_input).not_to_be_visible()

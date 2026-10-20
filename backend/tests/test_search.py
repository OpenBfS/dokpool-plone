from playwright.sync_api import expect

import pytest


class TestSearch:
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, playwright_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.page = playwright_page_factory()
        self.plone_url = self.portal.absolute_url()

    def test_search_context_dropdown_switch_event(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")

        page.locator("button.search-btn").click()
        expect(page.locator("#portal-searchbox")).to_be_visible()

        dropdown = page.locator("#search-context-dropdown-toggle")
        selected = page.locator("#search-context-scope-input")

        expect(dropdown).to_be_visible()
        expect(selected).to_have_value("current_event")

        search_input = page.locator("#searchGadget")
        search_input.fill("nonexistent search result")
        search_input.press("Enter")

        expect(page.locator("#listing")).to_be_visible()
        assert page.url.split("?", 1)[0] == f"{self.plone_url}/bund/@@listing"
        expect(page.locator("#listing .listing-item")).to_have_count(0)


def test_admin_search_is_not_covered(acceptance, site_owner_page_factory):
    plone_url = acceptance["portal"].absolute_url()
    page = site_owner_page_factory()
    page.goto(f"{plone_url}/bund/setActiveApp?app=elan")
    toolbar = page.locator("#edit-zone")
    expect(toolbar).to_be_visible()
    page.locator("button.search-btn").click()
    searchbox = page.locator("#portal-searchbox.show")
    expect(searchbox).to_be_visible()

    toolbar_bounds = toolbar.bounding_box()
    search_bounds = searchbox.bounding_box()
    assert toolbar_bounds is not None
    assert search_bounds is not None
    assert search_bounds["x"] >= toolbar_bounds["x"] + toolbar_bounds["width"]

    page.locator(".dp-search-dismiss").click()
    expect(searchbox).to_be_hidden()

    toolbar.locator(".toolbar-collapse").click()
    expect(toolbar.locator(".toolbar-expand")).to_be_visible()
    page.locator("button.search-btn").click()
    expect(searchbox).to_be_visible()

    toolbar_bounds = toolbar.bounding_box()
    search_bounds = searchbox.bounding_box()
    assert toolbar_bounds is not None
    assert search_bounds is not None
    assert search_bounds["x"] >= toolbar_bounds["x"] + toolbar_bounds["width"]

    page.locator(".dp-search-dismiss").click()
    expect(searchbox).to_be_hidden()

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

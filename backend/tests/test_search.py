from playwright.sync_api import expect
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

import pytest


class TestSearch:
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=SITE_OWNER_NAME, roles=["Manager"])
        self.page = playwright_page_factory(username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD)
        self.plone_url = self.portal.absolute_url()

    def test_search_context_dropdown_switch_event(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")

        page.locator("button.search-btn").click()
        expect(page.locator("#portal-searchbox")).to_be_visible()

        toggle = page.locator("#search-context-dropdown-toggle")
        menu = page.locator("#search-context-dropdown-menu")
        selected = page.get_by_role("button", name="Normalfall")

        expect(toggle).to_be_visible()
        expect(selected).to_have_text("Normalfall")
        toggle.click()

        notfall = menu.locator("a.dp-search-context-link", has_text="Notfall").first
        expect(notfall).to_be_visible()
        notfall.click()
        page.wait_for_load_state("networkidle")
        page.locator(".dp-search-dismiss").click()
        expect(page.locator("#portal-searchbox")).not_to_be_visible()

        page.reload()
        page.wait_for_load_state("networkidle")
        page.pause()
        selected_event_title = page.locator(
            "#docpool-header .event-card.event-switcher-detail .text-truncate",
        ).first
        expect(selected_event_title).to_have_text("Notfall")

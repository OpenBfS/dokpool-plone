from playwright.sync_api import expect
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

import pytest


class TestUI:
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=SITE_OWNER_NAME, roles=["Manager"])
        self.page = playwright_page_factory(username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD)
        self.plone_url = self.portal.absolute_url()

    def test_header_dropdown(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        expect(page.locator("#docpool-header .desktop-settings-infos")).to_be_visible()
        page.get_by_role("button", name="Info").click()
        info_dropdown = page.locator("#docpool-header .desktop-settings-infos .menu-info-dropdown")
        expect(info_dropdown.get_by_text("Softwareversion")).to_be_visible()

    def test_desktop_nav_switch_event(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")

        expect(page.locator("#docpool-header .desktop-settings-infos")).to_be_visible()
        selected_event_title = page.locator(
            "#docpool-header .event-card.event-switcher-detail .text-truncate",
        ).first
        expect(selected_event_title).to_have_text("Normalfall")

        event_switcher = page.locator("#docpool-header .event-switcher").first
        expect(event_switcher).to_be_visible()
        event_switcher.click()

        notfall_link = page.locator("#event-dropdown-menu a", has_text="Notfall").first
        expect(notfall_link).to_be_visible()
        notfall_link.click()
        page.wait_for_load_state("networkidle")

        expect(selected_event_title).to_have_text("Notfall")

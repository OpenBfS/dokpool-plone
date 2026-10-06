from playwright.sync_api import expect

import pytest


class TestUI:
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, playwright_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.page = playwright_page_factory()
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
        expect(page).to_have_url(f"{self.plone_url}/bund/@@listing")

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

        expect(page).to_have_url(f"{self.plone_url}/bund/@@overview")
        expect(selected_event_title).to_have_text("Notfall")

        page.goto(f"{self.plone_url}/bund/@@listing")
        event_switcher.click()
        notfall_link.click()
        expect(page).to_have_url(f"{self.plone_url}/bund/@@overview")

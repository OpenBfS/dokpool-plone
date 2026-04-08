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

from docpool.doksys.config import DOKSYS_APP
from docpool.elan.config import ELAN_APP
from playwright.sync_api import expect

import pytest
import transaction


class TestNavigation:
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, site_owner_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.docpool = self.portal["bund"]
        self.docpool.supportedApps = (ELAN_APP, DOKSYS_APP)
        transaction.commit()

        self.page = site_owner_page_factory()
        self.docpool_url = self.docpool.absolute_url()

    def test_app_switcher(self):
        page = self.page
        page.goto(f"{self.docpool_url}/setActiveApp?app={ELAN_APP}")
        expect(page).to_have_url(f"{self.docpool_url}/@@overview")

        app_switcher = page.locator("#docpool-header .app-switcher")
        expect(app_switcher).to_be_visible()
        app_switcher.click()

        app_menu = page.locator("#docpool-header .app-dropdown-menu")
        doksys_link = app_menu.get_by_role("link", name="IMIS Doksys")
        expect(doksys_link).to_be_visible()
        doksys_link.click()
        expect(page).to_have_url(f"{self.docpool_url}/@@listing")

        app_switcher.click()
        elan_link = app_menu.get_by_role("link", name="ELAN")
        expect(elan_link).to_be_visible()
        elan_link.click()
        expect(page).to_have_url(f"{self.docpool_url}/@@overview")

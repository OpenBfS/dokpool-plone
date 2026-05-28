from playwright.sync_api import expect
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from urllib.parse import parse_qs
from urllib.parse import urlparse

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

        selected = page.locator("#search-context-scope-select")

        expect(selected).to_be_visible()
        expect(selected).to_have_value("current_event")

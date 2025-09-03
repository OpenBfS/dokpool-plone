from playwright.sync_api import expect
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_NAME

import pytest


class TestUpdateNotification:
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=TEST_USER_NAME, roles=["Manager"])
        self.page = playwright_page_factory(username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD)
        self.plone_url = self.portal.absolute_url()

    def test_listing(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/listing")
        # Tests if the DPDocument exists
        page.screenshot(path="screenshots/listing.png")
        first_list_item = page.locator(".listing-item h2").first
        expect(first_list_item).to_have_text("Weatherinfo")
        # Publish the DPDocument
        page.get_by_role("button", name="⋮").click()
        page.locator("#workflow-transition-publish").click()
        status_msg = page.locator(".statusmessage-info").first
        expect(status_msg).to_contain_text(" Info: New review state for Weatherinfo: Published")

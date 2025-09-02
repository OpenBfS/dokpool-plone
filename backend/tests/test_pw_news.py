from playwright.sync_api import expect
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_NAME

import pytest


class TestPwNews:
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=TEST_USER_NAME, roles=["Manager"])
        self.page = playwright_page_factory(username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD)
        self.plone_url = self.portal.absolute_url()

    def test_news_listing(self) -> None:
        page = self.page
        page.goto(f"{self.plone_url}/bund/esd")
        expect(page.get_by_role("heading", name="Digitale Lagedarstellung"))

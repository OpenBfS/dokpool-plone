from groupsfolder_setup import GroupsFolderSetupMixin
from playwright.sync_api import expect

import pytest


class TestDPDocumentView(GroupsFolderSetupMixin):
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, playwright_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.page = playwright_page_factory()
        self.plone_url = self.portal.absolute_url()
        self.docpool = self.portal["bund"]
        self.setup_content()

    def test_delete_item(self):
        page = self.page
        entry = self.group_folder["weatherinfo-without-images"]
        page.goto(entry.absolute_url())

        expect(page.locator("h1")).to_have_text("Weatherinfo without images")
        page.locator("a[href*='/@@delete_confirmation']").click()

        heading = page.get_by_role(
            "heading",
            name="Do you really want to delete this object?",
            exact=False,
        )
        expect(heading).to_be_visible()
        page.get_by_role("button", name="Delete").click()

        expect(page).to_have_url(f"{self.plone_url}/bund/@@listing")
        expect(page.locator("#listing .listing-item")).to_have_count(1)
        expect(page.locator("#listing .listing-item", has_text="Weatherinfo without images")).to_have_count(0)

        status_messages = page.locator("#global_statusmessage .portalMessage")
        status_message = status_messages.first
        expect(status_message).to_be_visible()
        close_button = status_message.locator(".portal-message-close")
        close_button.click()
        expect(status_message).to_be_hidden()

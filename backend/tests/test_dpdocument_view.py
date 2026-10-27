from groupsfolder_setup import GroupsFolderSetupMixin
from playwright.sync_api import expect

import pytest


class TestDPDocumentView(GroupsFolderSetupMixin):
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, content_admin_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.page = content_admin_page_factory()
        self.plone_url = self.portal.absolute_url()
        self.docpool = self.portal["bund"]
        self.setup_content()

    def test_close_view_returns_to_group_folder(self):
        page = self.page
        origin = self.group_folder.absolute_url()
        page.goto(origin)
        expect(page).to_have_url(origin)
        page.locator("#listing .listing-item", has_text=self.entry1.title).locator("h3").click()
        expect(page.locator(".dp-document-header h1")).to_have_text(self.entry1.title)
        page.locator(".dp-document-header .back a").click()
        expect(page).to_have_url(origin)

    def test_close_edit_returns_to_group_folder(self):
        page = self.page
        origin = self.group_folder.absolute_url()
        page.goto(origin)
        expect(page).to_have_url(origin)
        item = page.locator("#listing .listing-item", has_text=self.entry1.title)
        item.get_by_role("button").click()
        item.get_by_role("link", name="Edit", exact=True).click()
        expect(page.locator("#form-widgets-IDublinCore-title")).to_have_value(self.entry1.title)
        page.locator(".dp-document-header .back a").click()
        expect(page).to_have_url(origin)

    def test_close_view_returns_to_entrytypes(self):
        page = self.page
        origin = f"{self.docpool.absolute_url()}/@@entrytypes"
        page.goto(origin)
        expect(page).to_have_url(origin)
        page.locator(".entrytype").filter(has=page.locator(".badge")).first.locator("a").click()
        page.locator("#listing .listing-item h3").first.click()
        expect(page.locator(".dp-document-header h1")).to_be_visible()
        page.locator(".dp-document-header .back a").click()
        expect(page).to_have_url(origin)

    def test_close_view_returns_to_tasks(self):
        page = self.page
        origin = f"{self.docpool.absolute_url()}/@@tasks"
        page.goto(origin)
        expect(page).to_have_url(origin)
        page.locator("#listing .listing-item", has_text=self.entry3.title).locator("h3").click()
        expect(page.locator(".dp-document-header h1")).to_have_text(self.entry3.title)
        page.locator(".dp-document-header .back a").click()
        expect(page).to_have_url(origin)

    @pytest.mark.flaky(reruns=2)
    def test_delete_item(self):
        page = self.page
        entry = self.group_folder["weatherinfo-without-images"]
        page.goto(entry.absolute_url())

        expect(page.locator("h1")).to_have_text("Weatherinfo without images")
        page.locator("a[href*='/@@delete_confirmation']").click()

        delete_button = page.locator("button[name='form.buttons.Delete']")
        expect(delete_button).to_be_visible()
        delete_button.click()

        expect(page).to_have_url(f"{self.plone_url}/bund/@@listing")
        expect(page.locator("#listing .listing-item")).to_have_count(2)
        expect(page.locator("#listing .listing-item", has_text="Weatherinfo without images")).to_have_count(0)

        status_messages = page.locator("#global_statusmessage .portalMessage")
        status_message = status_messages.first
        expect(status_message).to_be_visible()
        close_button = status_message.locator(".portal-message-close")
        close_button.click()
        expect(status_message).to_be_hidden()

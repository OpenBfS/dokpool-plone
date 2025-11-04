from docpool.api.browser.setup import add_user
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.utils import getScenariosForCurrentUser
from playwright.sync_api import expect
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.namedfile.file import NamedBlobImage

import os
import pytest
import transaction


class TestListing:
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=TEST_USER_NAME, roles=["Manager"])
        self.page = playwright_page_factory(username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD)
        self.plone_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.docpool = self.portal["bund"]
        self.setup_content()

    def setup_content(self):
        add_user(self.docpool, "user1", ["group1"], enabled_apps=["elan"])
        content = self.docpool["content"]
        assert content.keys() == ["Transfers", "Members", "Groups"]
        assert "user1" in content["Members"]
        assert "user1" not in self.portal["Members"]

        # assign app to groupfolder to make is show up in navigation (#5434)
        self.group_folder = content["Groups"]["bund_group1"]
        ILocalBehaviorSupport(self.group_folder).local_behaviors = ["elan"]
        self.group_folder.reindexObject(idxs=["apps_supported"])
        logout()
        login(self.portal, "user1")

        # create entry
        self.entry = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="A Weatherinfo",
            description="foo",
            docType="weatherinformation",
            local_behaviors=["elan"],
            scenarios=getScenariosForCurrentUser(),
        )
        assert self.entry.created_by == "user1 (Bund) <i>Group1 (Bund)</i>"
        # add attachments
        filename = os.path.join(os.path.dirname(__file__), "image.png")
        with open(filename, "rb") as f:
            FILE_DATA = f.read()

        api.content.create(
            container=self.entry,
            type="Image",
            title="Some Image",
            description="foo",
            image=NamedBlobImage(data=FILE_DATA, filename="image.png"),
        )
        api.content.create(
            container=self.entry,
            type="Image",
            title="Another Image",
            description="bar",
            image=NamedBlobImage(data=FILE_DATA, filename="image2.png"),
        )
        transaction.commit()

    def test_publish_dpdocument(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Tests if the DPDocument exists
        first_list_item = page.locator(".listing-item h2").first
        expect(first_list_item).to_have_text("A Weatherinfo")
        # Publish the DPDocument
        page.get_by_role("button", name="⋮").click()
        page.locator("#workflow-transition-publish").click()
        status_msg = page.locator(".statusmessage-info").first
        expect(status_msg).to_contain_text(" Info: New review state for A Weatherinfo: Published")

    def test_modal_open_close(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Open modal
        page.get_by_role("link", name="A Weatherinfo", exact=True).click()
        # Wait for modal to open
        page.wait_for_selector("div#pat-modal")
        expect(page.locator("div#pat-modal")).to_have_count(1)
        metadata = page.locator(".doc_metadata div").last
        expect(metadata).to_contain_text("Wetterinformation (WETTER UND TRAJEKTORIEN)")
        # Close modal
        page.get_by_role("button", name="Close").click()
        expect(page.locator("div.panel-content")).to_have_count(0)

    def test_wizard(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/@@dpdocument_wizard_1")
        expect(page.locator("#container_uid")).to_have_value(self.group_folder.UID())
        page.locator("#form-widgets-docType").select_option("notification")
        page.get_by_role("button", name="Next").click()
        page.locator("#form-widgets-IDublinCore-title").fill("Example Entry")
        page.locator('iframe[title="Rich Text Area"]').content_frame.get_by_label("Rich Text Area").fill(
            "Test text"
        )
        # TODO:
        # page.get_by_role("button", name="Attachments").set_input_files("SOMETHING")
        page.get_by_role("button", name="Next").click()

        expect(page.get_by_role("checkbox", name="Normalfall")).to_be_checked()
        expect(page.get_by_role("radio", name="Only for member of 'Group1 (")).to_be_checked()
        expect(page.get_by_role("radio", name="For all users of 'ELAN Bund'")).not_to_be_checked()
        page.get_by_role("radio", name="For all users of 'ELAN Bund'").click()
        page.get_by_role("button", name="Save").click()

        expect(page.get_by_role("heading", name="Example Entry")).to_be_visible()
        expect(page.locator("#content div").filter(has_text="Normalfall").nth(3)).to_be_visible()
        expect(page.get_by_text("Test text")).to_be_visible()

        page.goto(f"{self.plone_url}/bund/listing")
        expect(page.get_by_text("Example Entry")).to_be_visible()
